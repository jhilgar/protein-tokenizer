import { useState, useEffect, useRef } from 'react'
import protein from './assets/protein.svg'
import uniprot from './assets/uniprot.svg'
import './App.css'

import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';
import Stack from '@mui/material/Stack';
import Divider from '@mui/material/Divider';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

import { Console, Hook, Unhook } from 'console-feed'

function createData(
  name,
  calories,
  fat,
  carbs,
  protein,
) {
  return { name, calories, fat, carbs, protein };
}

const rows = [
  createData('Frozen yoghurt', 159, 6.0, 24, 4.0),
  createData('Ice cream sandwich', 237, 9.0, 37, 4.3),
  createData('Eclair', 262, 16.0, 24, 6.0),
  createData('Cupcake', 305, 3.7, 67, 4.3),
  createData('Gingerbread', 356, 16.0, 49, 3.9),
];

function App() {
  const handleClick = () => {
    var searchQuery = {
      'url': 'https://rest.uniprot.org/uniprotkb/search?format=fasta&query=%28Insulin+AND+%28reviewed%3Atrue%29+AND+%28organism_id%3A9823%29+AND+%28length%3A%5B350+TO+400%5D%29%29&size=500'
    }

    fetch(
      import.meta.env.VITE_BACKEND_URL + "/search", {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(searchQuery)
    }
    )
  }

  useEffect(() => {
    const eventSource = new EventSource(import.meta.env.VITE_BACKEND_URL + "/stream");
    eventSource.onopen = (m) => { "sse => connected", m };
    eventSource.onerror = (e) => console.log("sse => error connecting", e);
    eventSource.onmessage = (data) => { console.log("sse => ", data.data); };
    return () => eventSource.close();
  })

  const [logs, setLogs] = useState([])
  useEffect(() => {
    const hookedConsole = Hook(
      window.console,
      (log) => {
        setLogs((currLogs) => [...currLogs, log])
        var elem = document.getElementById("logs")
        setTimeout(() => {
          elem.scrollTop = elem.scrollHeight
        }, 100)
      },
      false
    )
    return () => Unhook(hookedConsole)
  }, [])

  return (
    <>
      <div id="logs" style={{ height: "70px", overflow: "auto" }}>
        <Console logs={logs} variant="dark" />
      </div>
      <div>
        <a href="https://react.dev" target="_blank">
          <img src={protein} className="logo react rotate" alt="Protein logo" />
        </a>
      </div>
      <center>
        <Stack direction="row" spacing={2}>
          <Card variant="outlined" sx={{ width: 400, bgcolor: 'lightgray' }}>
            <Box sx={{ p: 2 }}>
              <Stack direction="row" spacing={1}>
                <Typography color="text.secondary" variant="body2">
                  <TextField
                    label="Search query"
                    id="outlined-size-small"
                    defaultValue="Insulin & Something"
                    size="small"
                    disabled
                  />
                </Typography>
                <Button variant="contained" onClick={handleClick}>Search</Button></Stack>
            </Box>
            <Divider />
            <Box sx={{ p: 2 }}>
              Custom search functionality currently disabled.
            </Box>
          </Card>
          <Card variant="outlined" sx={{ width: 400, bgcolor: 'lightgray' }}>
            Search results:
          </Card>
        </Stack>

      </center>
    </>
  )
}

export default App