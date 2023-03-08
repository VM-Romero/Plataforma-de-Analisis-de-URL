import React, {useEffect, useState, useRef} from 'react';
import { useNavigate } from 'react-router-dom';
import { ProgressSpinner } from 'primereact/progressspinner';
import { Toast } from 'primereact/toast';
import imagen from '../images/www.png';
import '../Home.css';

export function Home() {

    const [url, setUrl] = useState('')
    const navigate = useNavigate();
    const [loading,setLoading] = useState(false);
    const [count,setCount] = useState(0);
    const [sampleId, setSampleId] = useState("");
    const toast = useRef(null);

    useEffect(()=>{
        setTimeout(async () => {
            const  response = await fetch(`http://localhost:5000/samples/${sampleId}`,{
            'method': 'GET',
            'headers': {
                'Content-Type': 'application/json'
            }
        });
        const res = await response.json();
        /* Checking if the sample has been processed. */
        if(res.representations.length > 0){
            setLoading(false);
            navigate(`/samples/${sampleId}`);
        }else{
            if(count > 0){
               setCount(count - 1); 
            }else{
                setLoading(false);
                toast.current.show({life: 3000, severity: 'error', summary: 'Error', detail: 'Timeout'});
            }
            
        }
        },4000);
    },[count]);
    
    /**
     * It takes the URL from the input field, sends it to the server, 
     * and then sets the state of the app to the loading screen
     * @param e - the event object
     */
    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await fetch(`http://localhost:5000/samples`,{
            'method': 'POST',
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': JSON.stringify({
                url 
            })
        })
        const data = await response.json();
        setSampleId(data.id);
        setLoading(true);
        setCount(10);
    }

    return(
        <div className="row">
            <div>
                <Toast ref={toast} position="bottom-left"></Toast>
            </div>
            <div>
                <img className="imagen-home" src={imagen} width='200' height='200' alt='imagen'/>
            </div>
            <form onSubmit={handleSubmit}>
                <div className="input-group mb-3">
                    <input 
                    type="url" 
                    onChange={e => setUrl(e.target.value)}
                    value = {url}
                    className="form-control" 
                    placeholder="e.g https://google.com" 
                    autoFocus 
                    required
                    />
                    <button className="btn btn-primary btn-block">
                        Scan
                    </button>
                </div>
            </form>
            {loading && <ProgressSpinner/>}
        </div>
    )
}