import Papa from 'papaparse';
import { useState, useEffect } from 'react';
import './App.css';
import CsvEditor from './components/CsvEditor/CsvEditor';
import { CsvData, CsvRow } from './types/csv';

const CSV_URL = 'https://media.githubusercontent.com/media/datablist/sample-csv-files/main/files/customers/customers-100.csv'
const MOCK_DATA = [
  ["Name", "Age", "Occupation", "Address", "Phone", "Email", "Interests"],
  ["Alice", "28", "Engineer", "123 Main St", "555-123-4567", "hoge@example.com", "Coding"],
  ["Bob", "32", "Designer", "456 Main St", "555-234-5678", "fuga@example.com", "Design"],
  ["Charlie", "22", "Student", "789 Main St", "555-345-6789", "piyo@example.com", "Design"]
];

function App() {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<CsvData | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      setError(null);

      try {
        const response = await fetch(CSV_URL, {
          headers: {
            'Content-Type': 'text/csv',
          }
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch CSV data: ${response.status} ${response.statusText}`);
        }

        const csvText = await response.text();
        const parsedData = Papa.parse<CsvRow>(csvText as string, { header: true, skipEmptyLines: true });

        if (parsedData.errors) {
          throw new Error(`Failed to parse CSV data: ${parsedData.errors}`);
        }

        setData(parsedData.data);
      } catch (err: unknown) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError('Unknown error occurred');
        }
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  // if error is not null, set mock data to show the component
  const csvEditor = error ? (
    <CsvEditor
      onUpload={(data) => console.log(data)}
      initialData={MOCK_DATA}
      editableColumns={['Occupation']}
    />
  ) : (
    <CsvEditor
      onUpload={(data) => console.log(data)}
      initialData={data ?? MOCK_DATA}
      editableColumns={['Occupation']}
    />
  );


  return (
    <div className="App">
      {isLoading && <div>Loading...</div>}
      {!isLoading && csvEditor}
    </div>
  );
}

export default App;
