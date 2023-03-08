import React from "react";
import { VirtualScroller } from 'primereact/virtualscroller';
import { classNames } from 'primereact/utils';


export function VTAnalysisPanel(props){

    /**
     * If there are no positive results, return a message saying so. 
     * If there are positive results,
     * return a virtual scroller with the results
     * @returns A virtual scroller with the positive results.
     */
    const positiveResults = () => {
        if((props.representation.positive.length === 0)){
            return(<h5 style={{color:'grey'}}>Without results...</h5>);
        }else{
            return(
                <VirtualScroller items={props.representation.positive} itemSize={50} itemTemplate={basicItemTemplate} />
            );
        }
    }
    /**
     * If there are no negative results, return a message saying so. 
     * If there are negative results,
     * return a virtual scroller with the negative results
     * @returns A virtual scroller with the items being the negative results.
     */
    const negativeResults = () => {
        if((props.representation.negative.length === 0)){
            return(<h5 style={{color:'grey'}}>Without results...</h5>);
        }else{
            return(
                <VirtualScroller items={props.representation.negative} itemSize={50} itemTemplate={basicItemTemplate} />
            );
        }
    }
    /**
     * If there are no unrated results, return a message saying so. 
     * If there are unrated results,
     * return a virtual scroller with the unrated results
     * @returns A virtual scroller with the unrated results.
     */
    const unratedResults = () => {
        if((props.representation.unrated.length === 0)){
            return(<h5 style={{color:'grey'}}>Without results...</h5>);
        }else{
            return(
                <VirtualScroller items={props.representation.unrated} itemSize={50} itemTemplate={basicItemTemplate} />
            );
        }
    }
    /**
     * It returns a div with a className of 'scroll-item p-3' 
     * and a style of { width: '50px' } if the
     * orientation is horizontal, or { height: '50px' } 
     * if the orientation is vertical
     * @param item - The item to render
     * @param options - {
     * @returns A function that returns a div with a className and style.
     */
    const basicItemTemplate = (item, options) => {
        const className = classNames('scroll-item p-3', {
            'odd': options.odd
        });
        const style = options.props.orientation === 'horizontal' ? { width: '50px' } : { height: '50px' };

        return <div className={className} style={style}>{item}</div>;
    }
    return(
        <div>
            <div>
                <h4>Analysis description</h4>
                <p fontSize="18">{props.representation.description}</p>
            </div>
            <br/>
            <h4>Potentially malicious</h4>
            
            {positiveResults()}
            <br/>
            <h4>Benign</h4>
            
            {negativeResults()}
            <br/>
            <h4>Unrated</h4>
            
            {unratedResults()}
        </div>

    )
}