import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Home } from './components/Home';
import { Sample } from './components/Sample';
import { Navbar } from './components/Navbar';
import { About } from './components/About';
import { SimilarSamples } from './components/SimilarSamples';

function App() {
  return (
    <Router>
      <Navbar/>
      <div className="container p-4">
        <Routes>
          <Route path='/' element={ <Home/> }/>
          <Route path='/samples/:id' element={<Sample/>}/>
          <Route path='/similares/:id' element={ <SimilarSamples/> }/>
          <Route path='/about' element={ <About/> }/>
        </Routes>
      </div>
    </Router>
  );
}

export default App;
