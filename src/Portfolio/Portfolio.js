import React from "react";
import PortfolioCard from "./PortfolioCard";
import Holotype  from "../Assets/Portfolio/HoloType.jpg";
import SpaceAttack from "../Assets/Portfolio/SpaceAttackDemo.gif";
import RocketBoost from "../Assets/Portfolio/RocketBoost.gif";

const data = 
    [
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
        
        <div class="album  bg-body-tertiary">
        <div>
        <h1 class="text-center py-5">Portfolio</h1>
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