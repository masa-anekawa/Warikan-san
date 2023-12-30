// CsvEditor.stories.tsx
import { StoryFn, Meta } from '@storybook/react';
import CsvEditor, { CsvEditorProps } from './CsvEditor';

const mockData = [
  ["Name", "Age", "Occupation"],
  ["Alice", "28", "Engineer"],
  ["Bob", "32", "Designer"],
  ["Charlie", "22", "Student"]
];


export default {
  title: 'CsvEditor',
  component: CsvEditor,
} as Meta;

const Template: StoryFn<CsvEditorProps> = (args) => <CsvEditor {...args} />;

export const Default = Template.bind({});
Default.args = {
  onUpload: (data) => console.log(data),
  initialData: mockData,
  editableColumns: ['Occupation']
};
