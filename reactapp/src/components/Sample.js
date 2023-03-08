import React, {useState, useEffect} from 'react';
import { useParams } from "react-router-dom"; 
import { TabViewDemo } from './TabViewDemo';
import { useNavigate } from 'react-router-dom';

export function Sample() {
    
    const params = useParams();
    /**const [sample, setSample] = useState({id:0,url:'',representations:[]});*/
    const [sample, setSample] = useState(null);
    const navigate = useNavigate();

    /**
     * It gets a sample from the database.
     * @param id - the id of the sample you want to get
     */
    const getSample = async (id) => {
        const response = await fetch(`http://localhost:5000/samples/${id}`,{
            'method': 'GET',
            'headers': {
                'Content-Type': 'application/json'
            }
        })
        const res = await response.json();
        console.log(res)
        setSample(res)
    }

    /**
     * It takes an id as a parameter, makes a GET request to the backend, 
     * and sets the response to the state of the component
     * @param id - the id of the sample you want to get the similar samples for
     */

    const goToSimilares = () => {

        navigate(`/similares/${sample.id}`);
    }

    /* A hook that is called after the first render. 
    * It is used to load data from the database. 
    */
    useEffect(() => {
        getSample(params.id);
    }, []); // Carga en primer renderizado

    
    return(
        <div>
            <div align="right">
                <button className="btn btn-primary btn-lg"
                onClick={goToSimilares}
                >
                    More like this
                </button>
            </div>
            {sample && <TabViewDemo sample={sample}/>}
        </div>
        
    )
}