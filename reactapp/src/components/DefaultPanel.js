import React from "react";
import JSONPretty from 'react-json-pretty';

export function DefaultPanel(props){

    return(
        <div>
            <JSONPretty id="json-pretty" data={props} mainStyle="line-height:1.3;color:#3D8FDB;background:#F1EDF2;overflow:auto;"></JSONPretty>
        </div>
    );
}