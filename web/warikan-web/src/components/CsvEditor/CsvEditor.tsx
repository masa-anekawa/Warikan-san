import React, { useState } from 'react';
import styles from './CsvEditor.module.css';

import useCsvSerializer from '../../hooks/useCsvSerializer';

export type CsvEditorProps = {
  onUpload?: (data: string) => void;
  initialData?: string[][];
  editableColumns: string[]
};

const CsvEditor: React.FC<CsvEditorProps> = ({ onUpload, initialData = [], editableColumns }) => {
  const [token, setToken] = useState<string>('');
  const [csvData, setCsvData] = useState<string[][]>(initialData);
  const { serializeCsvData } = useCsvSerializer();


  const handleUpload = () => {
    const serialized = serializeCsvData(csvData);
    if (onUpload) {
      onUpload(serialized);
    }
  };

  const handleDataChange = (value: string, row: number, col: number) => {
    const newData = [...csvData];
    newData[row][col] = value;
    setCsvData(newData);
  };

  const handleFetch = async () => {
    // Implement your async function to fetch the CSV data here. For now, just log the token.
    console.log(token);
  };

  return (
    <div className={styles['csv-editor-container']}>
      <h2>CsvEditor</h2>

      <div className={styles['input-group']}>
        <label htmlFor="token-input">Input Token:</label>
        <input
          id="token-input"
          className={styles['token-input']}
          type="text"
          placeholder="Enter token"
          value={token}
          onChange={(e) => setToken(e.target.value)}
        />
        <button className={`${styles.button} ${styles['fetch-button']}`} onClick={handleFetch}>Fetch</button>
      </div>

      <table className={styles['csv-table']}>
        <thead>
          <tr>
            {csvData[0]?.map((header, idx) => <th key={idx}>{header}</th>)}
          </tr>
        </thead>
        <tbody>
          {csvData.slice(1).map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.map((cell, cellIndex) => {
                // Check if the column is editable
                const isEditable = editableColumns.includes(csvData[0][cellIndex]);

                if (isEditable) {
                  return (
                    <td key={cellIndex}>
                      <input
                        type="text"
                        value={cell}
                        onChange={(e) => handleDataChange(e.target.value, rowIndex + 1, cellIndex)}
                        placeholder="Enter data"
                        title="Data Input"
                      />
                    </td>
                  )
                }else {
                  return <td key={cellIndex}>{cell}</td>;
                }})}
            </tr>
          ))}
        </tbody>
      </table>

      <button className={`${styles.button} ${styles['upload-button']}`} onClick={handleUpload}>Upload</button>
    </div>
  );
};

export default CsvEditor;
