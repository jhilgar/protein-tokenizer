import React from 'react';
import './App.css';
import QueryForm from './Query/QueryForm';

const Header = () => 
  <header className="App-header">
    Protein Tokenizer
  </header>


const App = () => 
<div className="App">
  <>
    <Header/>
    <QueryForm/>
  </>
</div>

export default App;
