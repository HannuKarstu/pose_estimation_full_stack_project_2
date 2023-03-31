import * as React from 'react';

export default function NumberDisplay(data, header) {
    return (
        <>
            <h2>{header}</h2>
            <div className="result">
                {data}
            </div>
        </>
    );
}