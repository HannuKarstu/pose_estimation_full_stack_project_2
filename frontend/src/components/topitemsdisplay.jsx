import * as React from 'react';

export default function TopItemsDisplay(data, header, tableHeaderNames, top) {

    function getTopItems(dict, top) {
        const arr = Object.entries(dict);
        arr.sort((a, b) => b[1] - a[1]);
        const topItems = arr.slice(0, top).map((item) => item);
        return topItems;
    }

    function createTableRows(topItems) {
        return topItems.map((item) => (
            <tr key={item[0]}>
                <td>{item[0]}</td>
                <td>{item[1]}</td>
            </tr>
        ));
    }

    function createTable(data, tableHeaderNames, top) {
        const topItems = getTopItems(data, top)

        return (<table>
            <thead>
                <tr>
                    <th>{tableHeaderNames[0]}</th>
                    <th>{tableHeaderNames[1]}</th>
                </tr>
            </thead>
            <tbody>{createTableRows(topItems)}</tbody>
        </table>)
    }


    const itemsTable = createTable(data, tableHeaderNames, top)

    return (
        <>
            <h2>{header}</h2>
            <div class="centered">
                {itemsTable}
            </div>

        </>
    );
}