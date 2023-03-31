import * as React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function Linechart(data, header) {
    const dates = Object.keys(data);
    const oldestDate = new Date(Math.min(...dates.map(date => new Date(date))));
    let newestDate = new Date(Math.max(...dates.map(date => new Date(date))));
    newestDate.setDate(newestDate.getDate() + 1);

    // Create an array of all dates between the oldest and newest dates
    const dateList = [];
    let currentDate = new Date(oldestDate);
    while (currentDate <= newestDate) {
        dateList.push(new Date(currentDate).toISOString().substring(0, 10));
        currentDate.setDate(currentDate.getDate() + 1);
    }

    const resultList = [];
    for (const date of dateList) {
        resultList.push({ date: date, amount: data[date] || 0 });
    }

    return (
        <>
            <h2>{header}</h2>
            <ResponsiveContainer width={"100%"} aspect={2} >
                <LineChart width={600} height={300} data={resultList}>
                    <CartesianGrid strokeDasharray="1 3" />
                    <XAxis dataKey="date" minTickGap={2} />
                    <YAxis allowDecimals={false} />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="amount" stroke="#8884d8" activeDot={{ r: 8 }} />
                </LineChart>
            </ResponsiveContainer>
        </>
    );
}