import React from "react";
import formatter from 'html-formatter';

export function BasicInfoPanel(props){
    /* Creating a list of `<li>` elements from the list of whois entries. */
    const listItems = props.representation.l_whois.map((w) =>  <li key={w}>{w}</li>);

    const checkRecursion = (props) => {

        try {
            
            return(
                <pre>{formatter.render(props.representation.content)}</pre>
            );
            
        } catch (error) {
            
            return(
                props.representation.content
            );
        }

    }

    return(
        <div>
            <h2>{props.representation.description}</h2>
            <h3>URL</h3>
            {props.representation.url}
            <h3>IP</h3>
            {props.representation.ip_add}
            <h3>Geolocation</h3>
            {props.representation.geo_loc}
            <h3>URL's characters length</h3>
            {props.representation.url_len}
            <h3>Top Level Domain</h3>
            {props.representation.tld}
            <h3>Whois</h3>
            <ul style={{ listStyleType: 'none' }}>{listItems}</ul>
            <h3>Uses HTTPS</h3>
            {props.representation.https}
            <h3>Label</h3>
            {props.representation.label}
            <h3>Raw content</h3>
            {checkRecursion(props)}
        </div>

    )
}