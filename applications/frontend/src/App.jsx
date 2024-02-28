import { useState, useEffect, useRef } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

import { Console, Hook, Unhook } from 'console-feed'

function App() {
  const [logs, setLogs] = useState([])
  const handleClick = () => { 
    var jsonData = {
      'url': 'https://rest.uniprot.org/uniprotkb/search?format=fasta&query=%28Insulin+AND+%28reviewed%3Atrue%29+AND+%28organism_id%3A9823%29+AND+%28length%3A%5B350+TO+400%5D%29%29&size=500'
    }
    fetch('http://localhost:8000/search',
    { method: 'POST', 
    mode: 'cors', 
    headers: {
      'Content-Type': 'application/json',
        'Accept': 'application/json'
    },
    body: JSON.stringify(jsonData)
    }
    )
  };

  useEffect(() => {
    const eventSource = new EventSource("http://localhost:8000/stream");
    eventSource.onopen = () => { };
    eventSource.onerror = (e) => console.log("error connecting to backend", e);
    eventSource.onmessage = (data) => console.log("backend message:", data.data);
    return () => eventSource.close();
  })

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
    <div id = "logs" style={{height: "100px", overflow: "auto" }}>
      <Console logs={logs} variant="dark" />
      </div>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      
        <button type="submit" onClick={handleClick}>Search</button>
    </>
  )
}

export default App
