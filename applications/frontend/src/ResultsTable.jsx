import React, { useEffect, useState } from "react";
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';


export default function DenseTable({ entries }) {
    return (
        <TableContainer component={Paper}>
            <Table sx={{ minWidth: 200 }} size="small" aria-label="a dense table">
                <TableHead>
                    <TableRow>
                        <TableCell>Time</TableCell>
                        <TableCell align="right">Result ID</TableCell>
                        <TableCell align="right">Results (max 200)</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                        <TableRow key={entries.timestamp} sx={{ '&:last-child td, &:last-child th': { border: 0 } }} >
                            <TableCell component="th" scope="row">{entries.timestamp}</TableCell>
                            <TableCell align="right">{entries.query_id}</TableCell>
                            <TableCell align="right">{entries.num_results}</TableCell>
                        </TableRow>
                </TableBody>
            </Table>
        </TableContainer>
    );
}