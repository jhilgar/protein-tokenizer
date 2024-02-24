import {FormEvent, ReactElement, useEffect, useState} from 'react';



export const QueryForm = (): ReactElement => {
    const [output, setOutput] = useState("");

    const submit = (e: FormEvent) => {
        e.preventDefault();
        const target = e.target as HTMLFormElement;
        const data = new FormData(target)

        fetch('/', {method: target.method, body: data})
            .then((res) => res.json())
            .then((data) => {
                setOutput(data.input_text)
            });
    }

    return (
        <section>
            Some random shit
        <form onSubmit={submit} method="post">
            <input name="query" />
            <button type="submit">Submit</button>
        </form>
        {output}
        </section>
    )
};

export default QueryForm;
