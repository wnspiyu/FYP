import React from 'react'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import { ChakraProvider } from '@chakra-ui/react'

//import LandingPage from './components/pages/LandingPage'
import LandingPageNew from './components/pages/LandingPageNew'
import LoginPage from './components/pages/LoginPage'
import RegisterPage from './components/pages/RegisterPage'
import ForgetPasswordPage from './components/pages/ForgetPasswordPage'
import HomePage from './components/pages/HomePage'
import Emission from './components/pages/Emission'
import './App.css'

export default function App() {
    return (
        <ChakraProvider>
            <Router>           
                <div>
                    <Switch>
                        <Route exact path="/" component={ LandingPageNew } />
                        <Route path="/login" component={ LoginPage } />
                        <Route path="/register" component={ RegisterPage } />
                        <Route path="/forget-password" component={ ForgetPasswordPage } />
                        <Route path="/home" component={ HomePage } />
                        <Route path="/data" component={ Emission } />
                    </Switch>
                    
                </div>
               
            </Router>
        </ChakraProvider>
       
    )
}


