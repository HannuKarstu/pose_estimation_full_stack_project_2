import * as React from 'react';
import { PieChart, Pie, Cell, Legend, ResponsiveContainer } from 'recharts';

export default function Piechart(data, header) {
    const generateColors = (numColors) => {
        const colors = [];
        for (let i = 0; i < numColors; i++) {
            const hue = i * (360 / numColors);
            colors.push(`hsl(${hue}, 70%, 50%)`);
        }
        return colors;
    };

    const COLORS = generateColors(Object.keys(data).length);

    const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
        const RADIAN = Math.PI / 180;
        const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
        const x = cx + radius * Math.cos(-midAngle * RADIAN);
        const y = cy + radius * Math.sin(-midAngle * RADIAN);

        return (
            <text x={x} y={y} fill="white" textAnchor="middle" dominantBaseline="central">
                {`${(percent * 100).toFixed(0)}%`}
            </text>
        );
    };


    return (
        <>
            <h2>{header}</h2>
            <ResponsiveContainer width={"100%"} aspect={1}>
                <PieChart>
                    <Pie
                        data={Object.entries(data).map(([name, value]) => ({ name, value }))}
                        dataKey="value"
                        nameKey="name"
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={renderCustomizedLabel}
                        outerRadius={80}
                        fill="#8884d8"
                    >
                        {Object.keys(data).map((_, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                    </Pie>
                    <Legend formatter={(value, entry) => `${value} (${entry.payload.value} pcs)`} />
                </PieChart>
            </ResponsiveContainer>
        </>
    );
}