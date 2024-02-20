import React from "react";
import PortfolioCard from "./PortfolioCard";
import Holotype  from "../Assets/Portfolio/HoloType.jpg";
import SpaceAttack from "../Assets/Portfolio/SpaceAttackDemo.gif";
import RocketBoost from "../Assets/Portfolio/RocketBoost.gif";
import ServiceApp from "../Assets/Portfolio/Services.png";

const data = 
    [
        {
            image: ServiceApp,
            name: "ServiceApp - Service Marketplace", 
            githubLink: "https://github.com/Alishahidi1997/ServiceApp"
        }, 
        {
        image: Holotype,
        name: "HoloType-AR-Based Educational Software ", 
        githubLink: "https://github.com/Alishahidi1997/HoloType"
    }, 
    {
        image: SpaceAttack,
        name: "Space Attack",
        githubLink: "https://github.com/Alishahidi1997/Space-Attack"
    },
    {
        image: RocketBoost,
        name: "Rocket Boost",
        githubLink: "https://github.com/Alishahidi1997/Rocket-Boost"
    }

    ]


let demos = data.map(function(item) {
    return <PortfolioCard image={item.image} name={item.name} githubLink={item.githubLink}/>;
  });
  

function Portfolio(){
    return(
        
        <div class="album  bg-body-tertiary py-4" id="Portfolio">
            <div>
                <h3 class="text-center py-3 " style={{ fontWeight: 'bold' }}>Portfolio</h3>
            </div>
            <div class="container">
                <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-3">
                    {demos}
                    <br/>
  
        
        </div>
    </div> 
    </div>
    
    
    )
}

export default Portfolio;