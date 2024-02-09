import React from 'react';
import Information from './AboutMe/Information';
import NavBar from './Header';
import Portfolio from './Portfolio/Portfolio';
import Footer from './Footer';
import Achievment from './Achievments/Achievment';
import { ScrollToSection } from './Header';

function App(){
    return (
        <div>
            <NavBar />
            <Information /> 
            <Portfolio />
            <Achievment />
            <Footer />  
        </div>
    
      
    )
    
}

export default App;