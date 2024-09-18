import './App.css'
import { Route, Routes } from "react-router-dom"
import RootLayout from "./layout/RootLayout"
import Home from "./page/Home/Home"
import Login from "./page/Login/Login"

function App() {

  return (
    <>
    <Routes>
        <Route path="/" element={<RootLayout />}>
          <Route index element={<Home />} />

        </Route>
          <Route path="/access/login" element={<Login />} />
      </Routes>
    </>
  )
}

export default App
