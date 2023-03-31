import React, { useEffect } from 'react';
import baseUrl from '../BackendUrl'
import Linechart from '../components/linechart';
import Piechart from '../components/piechart';
import NumberDisplay from '../components/numberdisplay';
import TopItemsDisplay from '../components/topitemsdisplay';


function Stats(props) {
    let rootState = props.rootState
    let handleRootStateChange = props.handleRootStateChange

    useEffect(() => {
        fetch(`${baseUrl}/stats`).then(res => res.json()).then(data => {
            console.log("Fetched stats", data)
            handleRootStateChange({
                "stats": {
                    "imageAmounts": data.image_amounts,
                    "modelAmounts": data.model_amounts,
                    "predictionDates": data.prediction_dates,
                    "totalResults": data.total_results
                }
            });
        });
    }, []);

    let stats = rootState["stats"]

    return (
        <div className="App">
            <h1>Stats</h1>
            {stats !== null ?
                <div class="container">
                    <div class="flex-container">
                        <div class="flex-child small">
                            {Piechart(stats.modelAmounts, "Models used")}
                        </div>

                        <div class="flex-child big">
                            {Linechart(stats.predictionDates, "Prediction dates")}
                        </div>
                    </div>
                    <div class="flex-container">
                        <div class="flex-child big">
                            {NumberDisplay(stats.totalResults, "Total results")}
                        </div>
                        <div class="flex-child small">
                            {TopItemsDisplay(stats.imageAmounts, "Top 5 filenames", ["Filename", "Amount"], 5)}
                        </div>
                    </div>
                </div>
                :
                null}
        </div>
    );
}

export default Stats;