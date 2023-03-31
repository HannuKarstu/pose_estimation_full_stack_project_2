import React, { useState, useEffect } from 'react';
import ResultModal from '../components/modal';
import DataTable from '../components/table';
import baseUrl from '../BackendUrl'


function Results(props) {
    let rootState = props.rootState
    let handleRootStateChange = props.handleRootStateChange

    let items = rootState["items"]

    const [showModal, setShowModal] = useState(false);
    const [activeItem, setActiveItem] = useState(null);
    const [activeImage, setActiveImage] = useState(null)

    useEffect(() => {
        fetch(`${baseUrl}/items`).then(res => res.json()).then(data => {
            console.log("Fetched list of items", data.items)
            data.items.forEach((item, index, array) => {
                item.date = new Date(parseInt(item['_id'].slice(0, 8), 16) * 1000)
            });

            handleRootStateChange({ "items": data.items });
        });
    }, []);

    const fetchResultImage = async (item) => {
        const res = await fetch(
            `${baseUrl}/files/${item["_id"]}?prediction=True`
        );

        const imageBlob = await res.blob();
        const imageObjectURL = URL.createObjectURL(imageBlob);
        setActiveImage(imageObjectURL);
    }

    function handleModalOpen(item) {
        setShowModal(true)
        setActiveItem(item)
        fetchResultImage(item)
    }

    function handleModalClose() {
        setShowModal(false)
        setActiveItem(null)
        setActiveImage(null)
    }

    return (
        <div className="App">
            <h1>Results</h1>
            {items ? DataTable(items, handleModalOpen) : null}
            {(activeItem && activeImage) ? ResultModal(showModal, activeItem, activeImage, handleModalClose) : null}

        </div>
    );
}

export default Results;