import { useCallback } from 'react';
import Papa from 'papaparse';
import { CsvData } from '../types/csv';


const useCsvSerializer = () => {
  const serializeCsvData = useCallback((data: CsvData): string => {
    return Papa.unparse(data);
  }, []);

  return { serializeCsvData };
};

export default useCsvSerializer;
