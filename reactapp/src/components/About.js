import React from 'react'
import imagen from '../images/skull.png';
import '../About.css'

export const About = () => {
    return(
        <div className="principal">
            <div className="imagen-about">
                <img src={imagen} width='200' height='200' alt='imagen'/>
            </div>

            <div className="titulo">
                <h1>Welcome to Evil URL!</h1>
                <h2>A URL analysis platform</h2>  
            </div>
            
            <div className="cuerpo">
                <p className="cuerpo-texto">
                    The aim of this project is to give people a tool to be aware of some 
                    threats when being online. <br/> 
                    To achieve this purpose, Evil URL provides 
                    an interface where you can analyze whichever URL you want. <br/>
                    The result is useful information, at low and medium level, of the analyzed webpage. <br/>

                    Be safe! :)
                </p>  
            </div>
             
        </div>
        
    )
}