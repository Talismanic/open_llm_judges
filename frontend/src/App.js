import React, { useState, useEffect } from "react";

const App = () => {
    const [archetypes, setArchetypes] = useState([]);
    const [selectedArchetype, setSelectedArchetype] = useState("");
    const [numAgents, setNumAgents] = useState(1);
    const [models, setModels] = useState([{ model_name: "", endpoint: "", api_key: "" }]);
    const [taskMeta, setTaskMeta] = useState("");
    const [task, setTask] = useState("");
    const [response, setResponse] = useState(null);
    const [showModal, setShowModal] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch("http://127.0.0.1:8000/api/archetypes/")
            .then((res) => res.json())
            .then((data) => setArchetypes(data.archetypes))
            .catch((err) => console.error("Error fetching archetypes:", err));
    }, []);

    const handleArchetypeChange = (e) => {
        const value = e.target.value;
        setSelectedArchetype(value);
        if (value === "1") {
            setNumAgents(1);
            setModels([{ model_name: "", endpoint: "", api_key: "" }]);
        } else {
            setNumAgents(1);
            setModels([{ model_name: "", endpoint: "", api_key: "" }]);
        }
    };

    const handleNumAgentsChange = (e) => {
        const value = parseInt(e.target.value);
        setNumAgents(value);
        setModels((prevModels) => {
            let newModels = [...prevModels];
            if (value > prevModels.length) {
                for (let i = prevModels.length; i < value; i++) {
                    newModels.push({ model_name: "", endpoint: "", api_key: "" });
                }
            } else {
                newModels = newModels.slice(0, value);
            }
            return newModels;
        });
    };

    const handleModelChange = (index, field, value) => {
        setModels((prevModels) => {
            const newModels = [...prevModels];
            newModels[index][field] = value;
            return newModels;
        });
    };

    const handleSubmit = async () => {
        setLoading(true);
        setError(null);

        if ((selectedArchetype === "2" || selectedArchetype === "3") && models.length !== numAgents) {
            setError("Number of agents must be equal to the number of models provided.");
            setShowModal(true);
            setLoading(false);
            return;
        }

        const payload = {
            archetype: parseInt(selectedArchetype),
            num_agents: numAgents,
            task_meta: taskMeta,
            task: task,
            worker_agent_models: models.map(model => ({
                model_name: model.model_name || "default_model",
                endpoint: model.endpoint || "http://host.docker.internal:11434/v1",
                api_key: model.api_key || "abc"
            }))
        };

        const controller = new AbortController();
        const timeoutId = setTimeout(() => {
            controller.abort();
            setError("Judge System did not respond swiftly");
            setShowModal(true);
            setLoading(false);
        }, 60000);

        try {
            const res = await fetch("http://127.0.0.1:8000/api/judge/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!res.ok) {
                throw new Error("API Error: " + res.statusText);
            }

            const data = await res.json();
            setResponse(data);
            setShowModal(true);
        } catch (error) {
            if (error.name === "AbortError") {
                setError("Judge System did not respond swiftly");
            } else {
                setError("An error occurred while processing the request.");
            }
            setShowModal(true);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={styles.container}>
            {loading && <div style={styles.loaderOverlay}><div style={styles.loader}></div></div>}

            <h2 style={styles.heading}>LLM Judge System</h2>

            <label style={styles.label}>Archetype:</label>
            <select style={styles.input} onChange={handleArchetypeChange} value={selectedArchetype}>
                <option value="">Select Archetype</option>
                {archetypes.map((arc) => (
                    <option key={arc.id} value={arc.id}>{arc.name}</option>
                ))}
            </select>

            {selectedArchetype && (
                <>
                    {(selectedArchetype === "2" || selectedArchetype === "3") && (
                        <>
                            <label style={styles.label}>Number of Agents:</label>
                            <input type="number" style={styles.input} value={numAgents} onChange={handleNumAgentsChange} min="1" />
                            <p style={styles.warningText}>⚠ Number of agents must match the number of models provided.</p>
                        </>
                    )}

                    {models.map((model, index) => (
                        <div key={index} style={styles.modelContainer}>
                            <h4>Model {index + 1}</h4>
                            <label style={styles.label}>Model Name:</label>
                            <input type="text" style={styles.input} value={model.model_name} onChange={(e) => handleModelChange(index, "model_name", e.target.value)} />

                            <label style={styles.label}>Endpoint:</label>
                            <input type="text" style={styles.input} placeholder="Default: http://host.docker.internal:11434/v1" value={model.endpoint} onChange={(e) => handleModelChange(index, "endpoint", e.target.value)} />

                            <label style={styles.label}>API Key:</label>
                            <input type="text" style={styles.input} placeholder="Default: abc" value={model.api_key} onChange={(e) => handleModelChange(index, "api_key", e.target.value)} />
                        </div>
                    ))}
                </>
            )}

            <label style={styles.label}>Task Meta:</label>
            <textarea style={styles.largeInput} value={taskMeta} onChange={(e) => setTaskMeta(e.target.value)} />

            <label style={styles.label}>Task:</label>
            <textarea style={styles.largeInput} value={task} onChange={(e) => setTask(e.target.value)} />

            <button style={styles.submitButton} onClick={handleSubmit} disabled={loading}>
                {loading ? "Submitting..." : "Submit"}
            </button>

            {showModal && (
                <div style={styles.modalOverlay}>
                    <div style={styles.modal}>
                        <h3>{error ? "Error" : "Response"}</h3>
                        {selectedArchetype === "3" ? (
                        <div>
                            <h4>Consensus Decision</h4>
                            <pre style={styles.responseText}>{response.consensus_decision}</pre>
                        </div>
                    ) : (
                        <div>
                            <h4>Worker Output</h4>
                            <pre style={styles.responseText}>{response.worker_output}</pre>
                            <h4>Judge Decision</h4>
                            <pre style={styles.responseText}>{response.judge_decision}</pre>
                        </div>
                    )}
                    <button style={styles.closeButton} onClick={() => setShowModal(false)}>Close</button>
                    </div>
                </div>
            )}

            
        </div>
    );
};

const styles = {
    container: {
        padding: "20px",
        maxWidth: "600px",
        margin: "auto",
        backgroundColor: "#e8f5e9",
        borderRadius: "10px",
        boxShadow: "0px 4px 8px rgba(0, 0, 0, 0.2)",
    },
    heading: {
        textAlign: "center",
        color: "#2e7d32",
    },
    label: {
        display: "block",
        fontWeight: "bold",
        marginTop: "10px",
    },
    input: {
        width: "100%",
        padding: "8px",
        margin: "5px 0",
        borderRadius: "5px",
        border: "1px solid #ccc",
    },
    largeInput: {
        width: "100%",
        height: "80px",
        padding: "8px",
        margin: "5px 0",
        borderRadius: "5px",
        border: "1px solid #ccc",
    },
    submitButton: {
        backgroundColor: "#2e7d32",
        color: "white",
        padding: "12px",
        border: "none",
        borderRadius: "5px",
        cursor: "pointer",
        fontSize: "16px",
        width: "100%",
        marginTop: "10px",
    },
    warningText: {
        color: "red",
        fontSize: "14px",
    },
    modelContainer: {
        border: "1px solid #ccc",
        padding: "10px",
        borderRadius: "5px",
        marginBottom: "10px",
    },
    loaderOverlay: {
        position: "fixed", top: 0, left: 0, width: "100%", height: "100%",
        backgroundColor: "rgba(0, 0, 0, 0.6)", display: "flex",
        alignItems: "center", justifyContent: "center"
    },
    loader: {
        width: "50px", height: "50px", borderRadius: "50%",
        border: "5px solid #fff", borderTopColor: "transparent",
        animation: "spin 1s linear infinite"
    },
    modalOverlay: { /* Fullscreen background */
        position: "fixed", top: 0, left: 0, width: "100%", height: "100%",
        backgroundColor: "rgba(0,0,0,0.5)", display: "flex",
        justifyContent: "center", alignItems: "center"
    },
    modal: {
        background: "#e8f5e9", padding: "20px", borderRadius: "10px",
        boxShadow: "0 4px 8px rgba(0,0,0,0.2)", width: "80%",
        maxWidth: "800px",
        maxHeight: "80vh",
        overflowY: "auto"
    },
    responseContainer: {
        display: "flex",
        flexDirection: "column",
        gap: "20px",
        marginBottom: "20px"
    },
    responseSection: {
        backgroundColor: "#fff",
        padding: "15px",
        borderRadius: "8px",
        boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
    },
    workerResponse: {
        marginBottom: "15px",
        padding: "10px",
        backgroundColor: "#f8f9fa",
        borderRadius: "6px"
    },
    responseText: {
        whiteSpace: "pre-wrap",
        wordWrap: "break-word",
        maxWidth: "100%",
        overflowX: "hidden",
        fontSize: "14px",
        backgroundColor: "#f5f5f5",
        padding: "10px",
        borderRadius: "4px",
        margin: "5px 0"
    },
    closeButton: {
        marginTop: "10px",
        backgroundColor: "#d32f2f",
        color: "white",
        padding: "10px",
        border: "none",
        borderRadius: "5px",
        cursor: "pointer",
    },
    "@keyframes spin": {
        "0%": { transform: "rotate(0deg)" },
        "100%": { transform: "rotate(360deg)" }
    }

};

export default App;
