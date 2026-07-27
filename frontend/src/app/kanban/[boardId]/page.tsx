// src/app/kanban/page.tsx
'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import {
  Box,
  AppBar,
  Toolbar,
  Typography,
  Button,
  Container,
  Grid,
  Paper,
  Card,
  CardContent,
  CardActions,
  Chip,
  IconButton,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Avatar,
  Divider,
  InputAdornment,
} from '@mui/material';
import {
  Add as AddIcon,
  Search as SearchIcon,
  ExitToApp as LogoutIcon,
  CalendarToday as CalendarIcon,
  Person as PersonIcon,
} from '@mui/icons-material';
import Cookies from 'js-cookie';
import logoImg from '@/assets/logo.png';
import Header from '@/components/Header';


type Priority = 'low' | 'medium' | 'high';
type ColumnId = 'todo' | 'in_progress' | 'review' | 'done';

interface Ticket {
  id: string;
  title: string;
  description: string;
  column: ColumnId;
  priority: Priority;
  dueDate: string;
  assignedTo: string;
}

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

export default function KanbanPage() {
  const router = useRouter();

  const [tickets, setTickets] = useState<Ticket[]>([
    {
      id: 'TK-101',
      title: 'Configurar rotas JWT no Django',
      description: 'Criar endpoints de obtain_token e refresh_token para a API REST.',
      column: 'done',
      priority: 'high',
      dueDate: '2026-07-28',
      assignedTo: 'Backend Dev',
    },
    {
      id: 'TK-102',
      title: 'Integrar Frontend Next.js com API',
      description: 'Implementar consumo via Axios com suporte a Bearer Token nos cookies.',
      column: 'in_progress',
      priority: 'high',
      dueDate: '2026-07-30',
      assignedTo: 'Frontend Dev',
    },
    {
      id: 'TK-103',
      title: 'Rastreamento de Transições de Coluna',
      description: 'Garantir que o histórico armazene a troca de estados do ticket.',
      column: 'todo',
      priority: 'medium',
      dueDate: '2026-08-02',
      assignedTo: 'Django Dev',
    },
    {
      id: 'TK-104',
      title: 'Testes de Carga na AWS',
      description: 'Validar ambiente de homologação implantado via GitHub Actions.',
      column: 'todo',
      priority: 'low',
      dueDate: '2026-08-05',
      assignedTo: 'DevOps',
    },
  ]);


  const [searchTerm, setSearchTerm] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);


  const [newTitle, setNewTitle] = useState('');
  const [newDesc, setNewDesc] = useState('');
  const [newPriority, setNewPriority] = useState<Priority>('medium');
  const [newColumn, setNewColumn] = useState<ColumnId>('todo');
  const [newDueDate, setNewDueDate] = useState('');


  const handleLogout = () => {
    Cookies.remove('access_token');
    Cookies.remove('refresh_token');
    router.push('/login');
  };

  const handleMoveTicket = (ticketId: string, targetColumn: ColumnId) => {
    setTickets((prev) =>
      prev.map((t) => (t.id === ticketId ? { ...t, column: targetColumn } : t))
    );
  };

  // Criar Novo Ticket
  const handleCreateTicket = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle) return;

    const newTicket: Ticket = {
      id: `TK-${Math.floor(100 + Math.random() * 900)}`,
      title: newTitle,
      description: newDesc,
      column: newColumn,
      priority: newPriority,
      dueDate: newDueDate || 'Sem data',
      assignedTo: 'Dev',
    };

    setTickets([...tickets, newTicket]);
    setIsModalOpen(false);

    // Reset Form
    setNewTitle('');
    setNewDesc('');
    setNewPriority('medium');
    setNewColumn('todo');
    setNewDueDate('');
  };

  // Helper de Cor para Badge de Prioridade
  const getPriorityChip = (priority: Priority) => {
    const config = {
      high: { label: 'Alta', color: 'error' as const },
      medium: { label: 'Média', color: 'warning' as const },
      low: { label: 'Baixa', color: 'success' as const },
    };
    const p = config[priority];
    return <Chip label={p.label} color={p.color} size="small" variant="outlined" />;
  };

  // Tickets Filtrados
  const filteredTickets = tickets.filter(
    (t) =>
      t.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      t.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      t.id.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <Box sx={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', bgcolor: 'background.default' }}>
      {/* 1. Header Principal */}
      <Header />

      {/* 2. Barra de Ferramentas e Filtros */}
      <Container maxWidth={false} sx={{ py: 3, flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            mb: 3,
            flexWrap: 'wrap',
            gap: 2,
          }}
        >
          <TextField
            placeholder="Pesquisar por ID, título ou descrição..."
            variant="outlined"
            size="small"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            sx={{ width: { xs: '100%', sm: 350 } }}
            slotProps={{
              input: {
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon color="action" />
                  </InputAdornment>
                )
              }
            }}
          />

          <Button
            variant="contained"
            color="primary"
            startIcon={<AddIcon />}
            onClick={() => setIsModalOpen(true)}
            sx={{ fontWeight: 'bold' }}
          >
            Novo Ticket
          </Button>
        </Box>

        {/* 3. Colunas do Kanban */}
        <Grid container spacing={3} sx={{ flexGrow: 1, alignItems: 'stretch' }}>
          {COLUMNS.map((col) => {
            const columnTickets = filteredTickets.filter((t) => t.column === col.id);

            return (
              <Grid item xs={12} sm={6} md={3} key={col.id} sx={{ display: 'flex' }}>
                <Paper
                  elevation={2}
                  sx={{
                    p: 2,
                    width: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    bgcolor: 'background.paper',
                    borderRadius: 2,
                  }}
                >
                  {/* Cabeçalho da Coluna */}
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                    <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                      {col.title}
                    </Typography>
                    <Chip label={columnTickets.length} color={col.color} size="small" sx={{ fontWeight: 'bold' }} />
                  </Box>

                  <Divider sx={{ mb: 2 }} />

                  {/* Cards da Coluna */}
                  <Box sx={{ flexGrow: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 2 }}>
                    {columnTickets.length === 0 ? (
                      <Box
                        sx={{
                          p: 3,
                          textAlign: 'center',
                          border: '1px dashed',
                          borderColor: 'divider',
                          borderRadius: 2,
                        }}
                      >
                        <Typography variant="caption" color="text.secondary">
                          Nenhum ticket nesta coluna
                        </Typography>
                      </Box>
                    ) : (
                      columnTickets.map((ticket) => (
                        <Card key={ticket.id} variant="outlined" sx={{ borderRadius: 2 }}>
                          <CardContent sx={{ pb: 1 }}>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                              <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 'bold' }}>
                                {ticket.id}
                              </Typography>
                              {getPriorityChip(ticket.priority)}
                            </Box>

                            <Typography variant="subtitle2" sx={{ mb: 0.5, fontWeight: 'bold' }}>
                              {ticket.title}
                            </Typography>

                            <Typography variant="body2" color="text.secondary" sx={{ mb: 1.5, fontSize: '0.8rem' }}>
                              {ticket.description}
                            </Typography>

                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, color: 'text.secondary' }}>
                              <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                <CalendarIcon sx={{ fontSize: 14 }} />
                                <Typography variant="caption">{ticket.dueDate}</Typography>
                              </Box>
                              <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                <PersonIcon sx={{ fontSize: 14 }} />
                                <Typography variant="caption">{ticket.assignedTo}</Typography>
                              </Box>
                            </Box>
                          </CardContent>

                          <CardActions sx={{ px: 2, pb: 1.5, pt: 0, justifyContent: 'flex-end' }}>
                            <FormControl size="small" sx={{ minWidth: 120 }}>
                              <Select
                                value={ticket.column}
                                onChange={(e) => handleMoveTicket(ticket.id, e.target.value as ColumnId)}
                                sx={{ fontSize: '0.75rem', height: 28 }}
                              >
                                {COLUMNS.map((c) => (
                                  <MenuItem key={c.id} value={c.id} sx={{ fontSize: '0.75rem' }}>
                                    {c.title}
                                  </MenuItem>
                                ))}
                              </Select>
                            </FormControl>
                          </CardActions>
                        </Card>
                      ))
                    )}
                  </Box>
                </Paper>
              </Grid>
            );
          })}
        </Grid>
      </Container>      
    </Box>
  );
}