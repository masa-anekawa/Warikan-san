// use hook that fetches csv data by downloading csv file from url or local file
import { useState, useEffect } from 'react';
import Papa from 'papaparse';
import { CsvData, CsvRow } from '../types/csv';

export type CsvFetchOptions = {
  url: string;
  headers?: Record<string, string>;
};

export type CsvFetchResult = {
  data: CsvData | null;
  message?: string;
  isLoading: boolean; // Add isLoading property to CsvFetchResult type
  error: string | null;
};

export const useCsvDataFetcher = (options: CsvFetchOptions): CsvFetchResult => {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<CsvData | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      setError(null);

      try {
        const response = await fetch(options.url, {
          headers: {
            'Content-Type': 'text/csv',
            ...options.headers
          }
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch CSV data: ${response.status} ${response.statusText}`);
        }

        const csvText = await response.text();
        const parsedData = Papa.parse<CsvRow>(csvText as string, { header: true, skipEmptyLines: true });

        if (parsedData.errors.length > 0) {
          throw new Error(`Failed to parse CSV data: ${parsedData.errors[0].message}`);
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
  }, [options]);

  return { data, isLoading, error };
};
