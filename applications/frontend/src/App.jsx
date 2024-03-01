import { useState, useEffect, useRef } from 'react'
import protein from './assets/protein.svg'

import { Console, Hook, Unhook } from 'console-feed'
import Stack from '@mui/material/Stack';

import './App.css'
import SearchCard from './SearchCard'

import TextField from '@mui/material/TextField';

function App() {
  const [searchResults, setSearchResults] = useState({ timestamp: '', query_id: '', num_results: 0 })
  const [tokenizerResults, setTokenizerResults] = useState(" ")
  useEffect(() => {
    const eventSource = new EventSource(import.meta.env.VITE_BACKEND_URL + "/stream");
    eventSource.onopen = (m) => { "sse => connected", m };
    eventSource.onerror = (e) => { console.error("sse => error connecting", e), eventSource.close() };
    eventSource.onmessage = (m) => {
      var data = JSON.parse(m.data)
      console.log(new Date().toLocaleString() + " :: rabbitmq :: ", data.source + " => " + data.destination)

      switch (data.source) {
        case 'datacollector':
          setSearchResults({
            timestamp: new Date().toLocaleTimeString(),
            query_id: data.query_id,
            num_results: data.num_results
          })
        case 'dataanalyzer':
          setTokenizerResults(data.tokenizer_json)
      }

    }
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
      <Stack spacing={3}>
          <div>
            <a href="https://react.dev" target="_blank">
              <img src={protein} className="logo react rotate" alt="Protein logo" />
            </a>
          </div>
          <div>
            protein tokenizer ::
            <a href="github.com/jhilgar/protein-tokenizer"> github.com/jhilgar/protein-tokenizer</a> ::
            u of colorado :: csca 5028 :: spring 1 :: final project
          </div>
          <center>
          <SearchCard entries={searchResults} />
          </center>
          <center>
          <TextField
            disabled
            id="outlined-multiline-static"
            label="Tokenizer Output"
            multiline
            rows={10}
            value={tokenizerResults}
            InputProps={{ style: { fontSize: 12 } }}
            InputLabelProps={{ style: { fontSize: 12 } }}
            sx={{ width: "350px" }}
          />
          </center>
          <div id="logs" style={{ height: "100px", overflow: "auto" }}>
            <Console logs={logs} variant="dark" />
          </div>
        
      </Stack>

    </>
  )
}

export default App