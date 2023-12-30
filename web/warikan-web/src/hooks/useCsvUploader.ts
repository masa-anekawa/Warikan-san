import { useState } from 'react';
import { CsvData } from '../types/csv';
import useCsvSerializer from './useCsvSerializer';

type CsvUploadResult = {
  success: boolean;
  message?: string;
};

type CsvUploadOptions = {
  url: string;
  headers?: Record<string, string>;
};

const useCsvUploader = () => {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const { serializeCsvData } = useCsvSerializer();

  const uploadCsvData = async (data: CsvData, options: CsvUploadOptions): Promise<CsvUploadResult> => {
    setIsLoading(true);
    setError(null);

    // log the data to the console for debugging
    console.log(serializeCsvData(data));

    try {
      const response = await fetch(options.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'text/csv',
          ...options.headers
        },
        body: serializeCsvData(data)
      });

      if (!response.ok) {
        throw new Error(`Failed to upload CSV data: ${response.status} ${response.statusText}`);
      }

      return { success: true };
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
        return { success: false, message: err.message };
      }
      setError('Unknown error occurred');
      return { success: false, message: 'Unknown error occurred' };
    } finally {
      setIsLoading(false);
    }
  };

  return { uploadCsvData, isLoading, error };
};

export default useCsvUploader;
