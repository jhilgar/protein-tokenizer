import { useState, useEffect, useRef } from 'react'
import protein from './assets/protein.svg'
import uniprot from './assets/uniprot.svg'
import './App.css'

import { Console, Hook, Unhook } from 'console-feed'
import {Card, CardHeader, CardBody, CardFooter, Divider, Link, Image} from "@nextui-org/react";

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
    eventSource.onopen = (m) => { "sse => connected", m};
    eventSource.onerror = (e) => console.log("sse => error connecting", e);
    eventSource.onmessage = (data) => console.log("sse => ", data.data);
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
    <div id = "logs" style={{height: "100px", overflow: "auto" }}>
      <Console logs={logs} variant="dark" />
      </div>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={uniprot} className="logo" alt="UniProt logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={protein} className="logo react" alt="Protein logo" />
        </a>
      </div>
      <h1>Protein tokenizer</h1>
      <p>A WIP</p>
      <button type="submit" onClick={handleClick}>Search</button>
      <Card className="max-w-[400px]">
      <CardHeader className="flex gap-3">
        <Image
          alt="nextui logo"
          height={40}
          radius="sm"
          src="https://avatars.githubusercontent.com/u/86160567?s=200&v=4"
          width={40}
        />
        <div className="flex flex-col">
          <p className="text-md">NextUI</p>
          <p className="text-small text-default-500">nextui.org</p>
        </div>
      </CardHeader>
      <Divider/>
      <CardBody>
        <p>Make beautiful websites regardless of your design experience.</p>
      </CardBody>
      <Divider/>
      <CardFooter>
        <Link
          isExternal
          showAnchorIcon
          href="https://github.com/nextui-org/nextui"
        >
          Visit source code on GitHub.
        </Link>
      </CardFooter>
    </Card>
    </>
  )
}

export default App