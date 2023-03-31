import * as React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';

const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: '90%',
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
};

export default function ResultModal(showModal, activeItem, activeImage, handleModalClose) {
    const modalTitle = "POSE ESTIMATION RESULT"
    const dateDisplayOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric', hour12: false };

    let modalText = <>
        Model Name: {activeItem["model_name"]} <br /><br />
        Date: {activeItem["date"].toLocaleDateString(undefined, dateDisplayOptions)} <br /><br />
        Filename: {activeItem["filename"]}
    </>


    return (
        <div>
            <Modal
                open={showModal}
                onClose={handleModalClose}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <Box sx={style}>
                    <Typography id="modal-modal-title" variant="h6" component="h2">
                        {modalTitle}
                    </Typography>
                    <Typography id="modal-modal-description" sx={{ mt: 2 }}>
                        <div class="flex-container">
                            <div class="flex-child left">
                                {modalText}
                            </div>
                            <div class="flex-child right">
                                <img
                                    src={activeImage}
                                    alt={activeItem.filename}
                                    className="photo"
                                />
                            </div>
                        </div>

                    </Typography>
                </Box>
            </Modal>
        </div>
    );
}