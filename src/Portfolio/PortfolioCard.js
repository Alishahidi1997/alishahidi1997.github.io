import React from "react";
import Icons from "../AboutMe/icons";
import {Github } from 'react-bootstrap-icons';
import { OverlayTrigger, Tooltip } from 'react-bootstrap';

function PortfolioCard(props){
  console.log(props.name);
  const tooltipText = "aaaa";
    return(
      <OverlayTrigger
      placement="top"
      overlay={<Tooltip id="tooltip-top">Click to redirect to GitHub repository</Tooltip>}
    >

        <a href={props.githubLink} style={{ textDecoration: 'none' }} target="_blank">
        <div class="col">
          <div class="card shadow-sm">
            <img src={props.image} height={250} alt={props.name}></img>
            <div class="card-body" >
              <p class="card-text text-center">{props.name}</p>
              <div class="d-flex justify-content-between align-items-center">     
              {/* <Icons  icon={Github} link={props.githubLink} altText="Github" /> */}
              </div>
            </div>
          </div>
        </div>
        </a>
        </OverlayTrigger>

    )
}

export default PortfolioCard;