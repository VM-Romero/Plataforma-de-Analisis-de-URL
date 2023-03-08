import React from "react";

export function VTInfoPanel(props){
    
    /* Creating a list of items from the categories array. */
    const listItems = props.representation.categories.map((c) =>  <li key={c}>{c}</li>);

    return(
        <div>
            <h2>{props.representation.description}</h2>
            <ul style={{ listStyleType: 'none' }}>{listItems}</ul>
        </div>

    )
}