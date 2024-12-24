// Create a React component
const App = () => {
    return React.createElement('h1', null, 'Hello, React in JavaScript!');
};
  
// Render the component to the DOM
ReactDOM.createRoot(document.getElementById('root')).render(React.createElement(App));
  