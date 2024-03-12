// This file is used to render the table in the admin dashboard
// The columns of the table are determined by the checkboxes selected


const tableDiv = document.getElementById('table');

        const updateUrl = (prev, query) => {
            return prev + (prev.indexOf('?') >= 0 ? '&' : '?') + new URLSearchParams(query).toString();
        };

        const editableCellAttributes = (data, row, col) => {
            if (row) {
                return {contentEditable: 'true', 'data-element-id': row.cells[0].data};
            }
            else {
                return {};
            }
        };

        const nameCheckbox = document.getElementById('nameCheckbox');
        const emailCheckbox = document.getElementById('emailCheckbox');
        const mobileCheckbox = document.getElementById('mobileCheckbox');
        const addressCheckbox = document.getElementById('addressCheckbox');
        const subscriptionCheckbox = document.getElementById('subscriptionCheckbox');
        const binCheckbox = document.getElementById('binCheckbox');
        const invoiceURLCheckbox = document.getElementById('invoiceURLCheckbox');

        let grid = new gridjs.Grid({
            columns: [
                { id: 'id', 'hidden': true },
                { id: 'address', name: 'Address', style: { width: '500px' }, 'attributes': editableCellAttributes },
                { id: 'subscription', name: 'Subscription', 'attributes': editableCellAttributes},
                { id: 'bin_collection', name: 'Bin Collection', 'attributes': editableCellAttributes},
                { id: 'name', name: 'Name', 'attributes': editableCellAttributes },
                { id: 'phone', name: 'Mobile', sort: false, 'attributes': editableCellAttributes },
                { id: 'email', name: 'Email', 'attributes': editableCellAttributes },
                { id: 'invoice_url', name: 'Download Invoice', formatter: (cell, row) => gridjs.h('a', { href: cell, target: '_blank' }, 'Download')}
            ],
            server: {
                url: '/search',
                then: results => results.data,
                total: results => results.total,
            },
            search: {
                enabled: true,
                server: {
                    url: (prev, search) => {
                    return updateUrl(prev, {search});
                    },
                },
            },
            sort: {
                enabled: true,
                multiColumn: true,
                server: {
                    url: (prev, columns) => {
                    const columnIds = ['id', 'address', 'subscriptions', 'name', 'phone', 'email'];
                    const sort = columns.map(col => (col.direction === 1 ? '+' : '-') + columnIds[col.index]);
                    return updateUrl(prev, {sort});
                    },
                },
            },
            pagination: {
                enabled: true,
                server: {
                    url: (prev, page, limit) => {
                    return updateUrl(prev, {start: page * limit, length: limit});
                    },
                },
            },
        }).render(tableDiv);


        function updateTable() {
            const columns = [];
            
            if (addressCheckbox.checked) {
                columns.push({ id: 'address', name: 'Address',
                    style: { width: '500px' }, 'attributes': editableCellAttributes });
            }
            if (subscriptionCheckbox.checked) {
                columns.push({ id: 'subscription', name: 'Subscription' });
            }
            if (binCheckbox.checked) {
                columns.push({ id: 'bin_collection', name: 'Bin' });
            }
            if (nameCheckbox.checked) {
                columns.push({ id: 'name', name: 'Name' });
            }
            if (emailCheckbox.checked) {
                columns.push({ id: 'email', name: 'Email' });
            }
            if (mobileCheckbox.checked) {
                columns.push({ id: 'phone', name: 'Mobile' });
            }
            if (invoiceURLCheckbox.checked) {
                columns.push({ id: 'invoiceURL', name: 'Invoice',
                formatter: (cell, row) => gridjs.h('a', { href: cell, target: '_blank' }, 'Open Invoice')});
            }

            grid.updateConfig({
                columns: columns,

                server: {
                    url: '/search',
                    then: results => results.data,
                    total: results => results.total,
                },
                search: {
                    enabled: true,
                    server: {
                        url: (prev, search) => {
                        return updateUrl(prev, {search});
                        },
                    },
                },
                sort: {
                    enabled: true,
                    multiColumn: true,
                    server: {
                        url: (prev, columns) => {
                        const columnIds = ['id', 'address', 'subscriptions', 'name', 'phone', 'email'];
                        const sort = columns.map(col => (col.direction === 1 ? '+' : '-') + columnIds[col.index]);
                        return updateUrl(prev, {sort});
                        },
                    },
                },
                pagination: {
                    enabled: true,
                    server: {
                        url: (prev, page, limit) => {
                        return updateUrl(prev, {start: page * limit, length: limit});
                        },
                    },
                },
                
            }).forceRender(tableDiv);

            let savedValue;

            tableDiv.addEventListener('focusin', ev => {
                if (ev.target.tagName === 'TD') {
                savedValue = ev.target.textContent;
                }
            });

            tableDiv.addEventListener('focusout', ev => {
                if (ev.target.tagName === 'TD') {
                if (savedValue !== ev.target.textContent) {
                    fetch('/api/data', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        id: ev.target.dataset.elementId,
                        [ev.target.dataset.columnId]: ev.target.textContent
                    }),
                    });
                }
                savedValue = undefined;
                }
            });

            tableDiv.addEventListener('keydown', ev => {
                if (ev.target.tagName === 'TD') {
                if (ev.key === 'Escape') {
                    ev.target.textContent = savedValue;
                    ev.target.blur();
                }
                else if (ev.key === 'Enter') {
                    ev.preventDefault();
                    ev.target.blur();
                }
                }
            });
        }

        // Call updateTable when a checkbox is clicked
        nameCheckbox.addEventListener('change', updateTable);
        emailCheckbox.addEventListener('change', updateTable);
        mobileCheckbox.addEventListener('change', updateTable);
        addressCheckbox.addEventListener('change', updateTable);
        subscriptionCheckbox.addEventListener('change', updateTable);
        binCheckbox.addEventListener('change', updateTable);
        invoiceURLCheckbox.addEventListener('change', updateTable);

        // Add event listeners for more checkboxes...

        // Initial table render
        updateTable();