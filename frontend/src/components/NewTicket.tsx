'use client';

import {
  Box,
  Button,
  Grid,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';


type Priority = 'low' | 'medium' | 'high';
type ColumnId = 'todo' | 'in_progress' | 'review' | 'done';

interface ColumnConfig {
  id: ColumnId;
  title: string;
  color: 'default' | 'primary' | 'warning' | 'success';
}

const COLUMNS: ColumnConfig[] = [
  { id: 'todo', title: 'A Fazer', color: 'default' },
  { id: 'in_progress', title: 'Em Progresso', color: 'primary' },
  { id: 'review', title: 'Em Revisão', color: 'warning' },
  { id: 'done', title: 'Concluído', color: 'success' },
];

export default function NewTicketModel() {
  return (
    <Dialog open={isModalOpen} onClose={() => setIsModalOpen(false)} fullWidth maxWidth="sm">
      <DialogTitle sx={{ fontWeight: 'bold' }}>Novo Ticket</DialogTitle>
      <Box component="form" onSubmit={handleCreateTicket}>
        <DialogContent dividers sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="Título"
            required
            fullWidth
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
          />

          <TextField
            label="Descrição"
            multiline
            rows={3}
            fullWidth
            value={newDesc}
            onChange={(e) => setNewDesc(e.target.value)}
          />

          <Grid container spacing={2}>
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel id="priority-label">Prioridade</InputLabel>
                <Select
                  labelId="priority-label"
                  label="Prioridade"
                  value={newPriority}
                  onChange={(e) => setNewPriority(e.target.value as Priority)}
                >
                  <MenuItem value="low">Baixa</MenuItem>
                  <MenuItem value="medium">Média</MenuItem>
                  <MenuItem value="high">Alta</MenuItem>
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel id="column-label">Coluna Inicial</InputLabel>
                <Select
                  labelId="column-label"
                  label="Coluna Inicial"
                  value={newColumn}
                  onChange={(e) => setNewColumn(e.target.value as ColumnId)}
                >
                  {COLUMNS.map((c) => (
                    <MenuItem key={c.id} value={c.id}>
                      {c.title}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          </Grid>

          <TextField
            label="Data Limite (Prazo)"
            type="date"
            fullWidth
            slotProps={{
              inputLabel: {
                shrink: true
              }
            }}
            value={newDueDate}
            onChange={(e) => setNewDueDate(e.target.value)}
          />
        </DialogContent>

        <DialogActions sx={{ p: 2 }}>
          <Button onClick={() => setIsModalOpen(false)} color="inherit">
            Cancelar
          </Button>
          <Button type="submit" variant="contained" color="primary">
            Salvar Ticket
          </Button>
        </DialogActions>
      </Box>
    </Dialog>
  )
}