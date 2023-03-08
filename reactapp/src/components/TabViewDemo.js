import 'primeicons/primeicons.css';
import 'primereact/resources/themes/lara-light-indigo/theme.css';
import 'primereact/resources/primereact.css';
import 'primeflex/primeflex.css';
import '../index.css';
import React, { useState } from 'react';
import { VTAnalysisPanel } from './VTAnalysisPanel';
import { VTInfoPanel } from './VTInfoPanel';
import { BasicInfoPanel } from './BasicInfoPanel';
import { DefaultPanel } from './DefaultPanel';
import Chart from 'react-apexcharts'
import { TabView, TabPanel } from 'primereact/tabview';

import '../TabViewDemo.css';


export function TabViewDemo(props) {
    /**
     * If the representation name is "VT analysis", return the VTAnalysisPanel 
     * component. If the representation name is "VT info", 
     * return the VTInfoPanel component. If the representation name is "Basic info", 
     * return the BasicInfoPanel component. Otherwise, return the DefaultPanel component
     * @param representation - The representation object that is passed to the renderer.
     * @returns A function that takes a representation as an argument and 
     * returns a panel based on the name of the representation.
     */
    const representationRenderer = (representation) => {
        if(representation.name === "VT analysis"){
            return(<VTAnalysisPanel representation={representation}/>)
        }else if (representation.name === "VT info"){
            return(<VTInfoPanel representation={representation}/>)
        }else if (representation.name === "Basic info"){
            return(<BasicInfoPanel representation={representation}/>)
        }else{
            return(<DefaultPanel representation={representation}/>)
        }

    }

    const countSubtypes = (sample) => {
        if(sample !== undefined){

            for (const r of sample.representations){
                if(r.name === "VT analysis"){
                    return([r.positive.length, r.negative.length, r.unrated.length]);
                }
            }

        }
        return([0,0,0]);
        
    }

    const [activeIndex2, setActiveIndex2] = useState(0);


    const analyzersTabs = Array.from(props.sample.representations, (r) => ({ name: r.name, representation: r }));
    
    return (
        <div>
            
            <div>
                <Chart
                    type="pie"
                    width={350}
                    height={350}
                    
                    series={countSubtypes(props.sample)}

                    options={{
                        title:{text:"Analysis stats for VT Analysis"},
                        noData:{text:"No data"},
                        labels:['Positive','Negative','Unrated']
                    }}
                />
            </div>
            <div className="tabview-demo">
                <div className="card">
                    <TabView activeIndex={activeIndex2} onTabChange={(e) => setActiveIndex2(e.index)} scrollable>
                        {analyzersTabs.map((tab) => {
                            return (
                                <TabPanel key={tab.name} header={tab.name}>
                                    {representationRenderer(tab.representation)}
                                </TabPanel>
                            )
                        })}
                    </TabView>
                </div>
            </div>
        </div>
        
    )
}
            