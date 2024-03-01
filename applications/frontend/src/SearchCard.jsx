import Card from '@mui/material/Card';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';
import Divider from '@mui/material/Divider';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

import ResultsTable from './ResultsTable'

const handleClick = () => {
    var searchQuery = {
        'query': document.getElementById('searchfield').value,
        'source': 'backend',
        'destination': 'datacollector'
    }

    fetch(
        import.meta.env.VITE_BACKEND_URL + "/search", {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(searchQuery)
    }
    )
}

const handleTrainClick = () => {
    var trainCommand = {
        source: "backend",
        destination: "dataanalyzer",
        query_id: 1,
        type: 'BPE',
        params: {
            vocab_size: 30,
            unk_token: "[UNK]",
            special_tokens: ["[CLS]", "[MASK]", "[PAD]"]
        }
    }

    fetch(
        import.meta.env.VITE_BACKEND_URL + "/train", {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(trainCommand)
    }
    )
}

export default function SearchCard({ entries }) {
    return (
        <Card variant="outlined" sx={{ width: 600 }}>
            <Box sx={{ p: 2 }}>
                <Stack direction="row" spacing={1}>
                    <Typography component={'span'} color="text.secondary" variant="body2">
                        <TextField
                            label="UniProtKB query"
                            id="searchfield"
                            size="small"
                            defaultValue="kappa immunoglobulin human"
                            style={{ width: 365 }}
                        />
                    </Typography>
                    <Button variant="contained" onClick={handleClick}>Search</Button>
                    <Button variant="contained" onClick={handleTrainClick}>Train BPE</Button>
                </Stack>
            </Box>
            <Divider />
            <Box sx={{ p: 2 }}>
                <ResultsTable entries={entries} />
            </Box>
        </Card>
    );
}