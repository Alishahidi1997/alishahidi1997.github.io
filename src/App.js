import React from 'react';
import Information from './AboutMe/Information';
import NavBar from './Header';
import Portfolio from './Portfolio/Portfolio';
import Footer from './Footer';

function App(){
    return <div>
        <NavBar />
        <Information /> 
        <div class="bg-body-tertiary">
            <Portfolio />
            <Footer /> 
        </div>
    </div>
    
}

export default App;