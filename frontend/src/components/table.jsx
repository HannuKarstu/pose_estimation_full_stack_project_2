import * as React from 'react';
import { DataGrid } from '@mui/x-data-grid';

const columns = [
    { field: 'date', headerName: 'Date', flex: 1 },
    { field: '_id', headerName: 'ID', flex: 1 },
    { field: 'model_name', headerName: 'Model', flex: 1 },
    { field: 'filename', headerName: 'Filename', flex: 1 }
];

export default function DataTable(rows, handleModalOpen) {
    return (
        <div style={{ height: 400, width: '100%' }}>
            <DataGrid
                rows={rows}
                columns={columns}
                pageSize={10}
                rowsPerPageOptions={[10]}
                checkboxSelection={false}
                getRowId={(row) => row._id}
                onRowClick={(row) => handleModalOpen(row.row)}
                disableSelectionOnClick={true}
            />
        </div>
    );
}