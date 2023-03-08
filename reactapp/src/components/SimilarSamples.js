import React, { useEffect, useState } from 'react';
import { useParams } from "react-router-dom"; 
import { useNavigate } from 'react-router-dom';
import { Rating } from 'primereact/rating'
import '../SimilarSamples.css'

export function SimilarSamples(props) {

    const params = useParams();
    const [similares, setSimilares] = useState([]);
    const navigate = useNavigate();

    const getSimilares = async (id) => {
        const response = await fetch(`http://localhost:5000/similares/${id}`,{
            'method': 'GET',
            'headers': {
                'Content-Type': 'application/json'
            }
        })
        const res = await response.json();
        console.log(res)
        setSimilares(res)
    }

    useEffect(() => {
        getSimilares(params.id);
    }, [params.id]);
    
    
    return(
        <div className="container-similar">
                <div className="card-similar">
                        <table summary="Similar webpages">
                            <caption>Similar webpages to the given one</caption>
                            <thead>
                                <tr>
                                    <th key="score">Score</th>
                                    <th key="url">URL</th>
                                </tr>
                            </thead>
                            
                            <tbody>
                                {similares.map(sim => (
                                    <tr>
                                        <td key={sim.score}>
                                            <Rating 
                                                value={5.0 * sim.score} 
                                                readOnly stars={5} 
                                                cancel={false}
                                            /> 
                                        </td>
                                        <td key={sim.id}><h6 onClick={() => navigate(`/samples/${sim.id}`)}>{sim.url}</h6></td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                </div>
        </div>
    );
}