import { React, useEffect } from 'react';
import Select from 'react-select'
import { Button } from '@mui/material';
import baseUrl from '../BackendUrl'


function Prediction(props) {
    let rootState = props.rootState
    let handleRootStateChange = props.handleRootStateChange

    let predicting = rootState["predicting"]
    let predictionResult = rootState["predictionResult"]
    let selectedFile = rootState["selectedFile"]
    let selectedModel = rootState["selectedModel"]
    let modelOptions = rootState["modelOptions"]

    useEffect(() => {
        handleRootStateChange({
            "predicting": null,
            "predictionResult": null,
            "selectedFile": null,
            "selectedModel": null
        })

        if (!modelOptions) {
            fetch(`${baseUrl}/models`).then(res => res.json()).then(data => {
                console.log("Fetched models", data)
                let options = data.models.map(model => ({ value: model, label: model }))
                handleRootStateChange({ "modelOptions": options });
            });
        }
    }, []);

    const handlePrediction = async () => {
        handleRootStateChange({ "predicting": "Predicting...", "predictionResult": null })

        const formData = new FormData();

        formData.append('file', selectedFile)
        const res = await fetch(
            `${baseUrl}/predict?model_name=${selectedModel}`,
            {
                method: 'POST',
                body: formData,

            }
        );

        const imageBlob = await res.blob();
        const imageObjectURL = URL.createObjectURL(imageBlob);
        handleRootStateChange({ "predicting": null, "predictionResult": imageObjectURL });
    }

    function predictedImage() {
        return (<>
            {predictionResult ? <img
                src={predictionResult}
                alt="predictionResult"
                className="photo"
            /> : predicting}
        </>
        )
    }

    function predictionOptions() {
        const modelSelectBox = () => {
            return (
                <Select
                    options={rootState["modelOptions"]}
                    onChange={(e) => handleRootStateChange({ "selectedModel": e.value })}
                    value={rootState["selectedModel"] ? rootState["selectedModel"].value : null}
                    placeholder="Select model"
                />
            )
        }

        const selectImageButton = () => {
            return (
                <Button
                    variant="contained"
                    component="label">
                    Select image
                    <input
                        hidden accept="image/*"
                        multiple type="file"
                        onChange={(e) => handleRootStateChange({ "selectedFile": e.target.files[0] })}
                    />
                </Button>
            )
        }

        const predictButton = () => {
            return (
                <Button
                    variant="contained"
                    onClick={handlePrediction}>
                    Predict
                </Button>
            )
        }

        return (
            <>
                {modelSelectBox()}
                <br />
                {selectImageButton()}
                <br />
                {selectedFile ? selectedFile.name : null}
                <br />
                <br />
                <br />
                {predictButton()}

            </>
        )
    }

    return (
        <div class="App">
            <h1>Prediction</h1>
            <div class="flex-container">
                <div class="flex-child">
                    {predictionOptions()}
                </div>
                <div class="flex-child">
                    {predictedImage()}
                </div>
            </div>

        </div>
    );
}

export default Prediction;