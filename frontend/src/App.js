import React, { useState } from 'react';
import './App.css';

import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./pages/Layout";
import Results from "./pages/Results";
import Prediction from "./pages/Prediction";
import Stats from "./pages/Stats";

function App() {
  const initialState = {
    "items": null,
    "loadingItems": false,
    "predicting": null,
    "predictionResult": null,
    "selectedFile": null,
    "selectedModel": null,
    "modelOptions": null,
    "version": null,
    "stats": null
  }

  const [state, setState] = useState(initialState)

  function handleStateChange(change) {
    console.log("Previous state", state)
    console.log("Change", change)
    let newState = Object.assign({}, state, change);
    console.log("New state", newState)
    setState(newState)
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Results rootState={state} handleRootStateChange={handleStateChange} />} />
          <Route path="prediction" element={<Prediction rootState={state} handleRootStateChange={handleStateChange} />} />
          <Route path="stats" element={<Stats rootState={state} handleRootStateChange={handleStateChange} />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;