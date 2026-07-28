'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Image from 'next/image';
import {
  Box,
  AppBar,
  Toolbar,
  Typography,
  Button,
  Paper,
  Card,
  CardContent,
  Chip,
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
  CircularProgress,
  Alert,
  IconButton,
} from '@mui/material';
import {
  Add as AddIcon,
  Search as SearchIcon,
  ArrowBack as ArrowBackIcon,
  ExitToApp as LogoutIcon,
  CalendarToday as CalendarIcon,
  SwapHoriz as MoveIcon,
} from '@mui/icons-material';
import api from '@/services/api';
import { useAuth } from '@/context/AuthContext';
import logoImg from '@/assets/logo.png';
import Header from '@/components/Header';

// Interfaces espelhando os dados do Django REST
export interface Ticket {
  id: number;
  number: number;
  formatted_number: string;
  title: string;
  description: string;
  priority: number;
  due_date: string | null;
  column: number;
  column_board_id: number;
  position: number;
  owner: number;
  shared_users: number[];
  created_at: string;
  updated_at: string;
}

export interface Column {
  id: number;
  name: string;
  position: number;
  color: string;
  board: number;
  tickets: Ticket[];
  created_at: string;
  updated_at: string;
}

export interface BoardDetail {
  id: number;
  name: string;
  description: string;
  color: string;
  owner: number;
  columns: Column[];
  created_at: string;
  updated_at: string;
}

export default function BoardDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { user, logout } = useAuth();
  const boardId = params.boardId as string;

  const [board, setBoard] = useState<BoardDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');

  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [selectedColumnId, setSelectedColumnId] = useState<number | ''>('');
  const [newTitle, setNewTitle] = useState('');
  const [newDescription, setNewDescription] = useState('');
  const [newPriority, setNewPriority] = useState<number>(11);
  const [newDueDate, setNewDueDate] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const [isMoveModalOpen, setIsMoveModalOpen] = useState(false);
  const [ticketToMove, setTicketToMove] = useState<Ticket | null>(null);
  const [targetColumnId, setTargetColumnId] = useState<number | ''>('');

  const fetchBoardDetails = useCallback(async () => {
    if (!boardId) return;
    setLoading(true);
    setError(null);
    try {
      const response = await api.get<BoardDetail>(`/tickets/board/${boardId}/`);
      setBoard(response.data);
    } catch (err: any) {
      console.error('Erro ao carregar detalhes do quadro:', err);
      setError('Não foi possível carregar as informações deste quadro.');
    } finally {
      setLoading(false);
    }
  }, [boardId]);

  useEffect(() => {
    fetchBoardDetails();
  }, [fetchBoardDetails]);

  const handleCreateTicket = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim() || !selectedColumnId) return;

    setIsSubmitting(true);
    try {
      await api.post('/tickets/ticket/', {
        title: newTitle,
        description: newDescription,
        priority: Number(newPriority),
        due_date: newDueDate || null,
        column: selectedColumnId,
      });

      setIsCreateModalOpen(false);
      setNewTitle('');
      setNewDescription('');
      setNewPriority(30);
      setNewDueDate('');
      setSelectedColumnId('');

      fetchBoardDetails();
    } catch (err) {
      console.error('Erro ao criar ticket:', err);
      alert('Erro ao criar a tarefa. Verifique os campos.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleMoveTicket = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!ticketToMove || !targetColumnId) return;

    setIsSubmitting(true);
    try {
      await api.post(`/tickets/ticket/${ticketToMove.id}/move/`, {
        to_column_id: targetColumnId,
      });

      setIsMoveModalOpen(false);
      setTicketToMove(null);
      setTargetColumnId('');

      fetchBoardDetails();
    } catch (err) {
      console.error('Erro ao mover ticket:', err);
      alert('Não foi possível mover o ticket.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const openCreateModalForColumn = (columnId: number) => {
    setSelectedColumnId(columnId);
    setIsCreateModalOpen(true);
  };

  const openMoveModal = (ticket: Ticket) => {
    setTicketToMove(ticket);
    setTargetColumnId(ticket.column);
    setIsMoveModalOpen(true);
  };

  const userDisplayName = user
    ? user.first_name ? `${user.first_name} ${user.last_name}`.trim() : user.username
    : 'Usuário';

  return (
    <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column', bgcolor: 'background.default', overflow: 'hidden' }}>
      <Header title={board?.name || 'Carregando...'}/>

      <Box sx={{ p: 2, bgcolor: 'background.paper', borderBottom: 1, borderColor: 'divider', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 2 }}>
        <Box>
          <Typography variant="body2" color="text.secondary">
            {board?.description || 'Quadro de acompanhamento de tarefas.'}
          </Typography>
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <TextField
            placeholder="Filtrar tarefas neste quadro..."
            size="small"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            sx={{ width: 280 }}
            slotProps={{
              input: {
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon color="action" fontSize="small" />
                  </InputAdornment>
                ),
              }
            }}
          />
        </Box>
      </Box>

      <Box
        sx={{
          flexGrow: 1,
          p: 3,
          display: 'flex',
          flexDirection: 'row',
          gap: 3,
          overflowX: 'auto',
          overflowY: 'hidden',
          alignItems: 'stretch',
          // bgcolor: '#f4f5f7',
        }}
      >
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', width: '100%' }}>
            <CircularProgress />
          </Box>
        ) : error ? (
          <Alert severity="error" sx={{ width: '100%', maxHeight: 60 }}>
            {error}
          </Alert>
        ) : (
          board?.columns?.map((column) => {
            const filteredTickets = column.tickets.filter((ticket) =>
              ticket.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
              ticket.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
              ticket.formatted_number.toLowerCase().includes(searchTerm.toLowerCase())
            );

            return (
              <Paper
                key={column.id}
                elevation={1}
                sx={{
                  width: 320,
                  minWidth: 320,
                  // bgcolor: '#ebecf0',
                  borderRadius: 2,
                  display: 'flex',
                  flexDirection: 'column',
                  maxHeight: '100%',
                  borderTop: `4px solid ${column.color || '#3B82F6'}`,
                }}
              >
                <Box sx={{ p: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                      {column.name}
                    </Typography>
                    <Chip label={filteredTickets.length} size="small" sx={{ height: 20, fontSize: '0.75rem', fontWeight: 'bold' }} />
                  </Box>

                  <Button
                    size="small"
                    startIcon={<AddIcon />}
                    onClick={() => openCreateModalForColumn(column.id)}
                    sx={{ textTransform: 'none' }}
                  >
                    Adicionar
                  </Button>
                </Box>

                <Box
                  sx={{
                    p: 1.5,
                    flexGrow: 1,
                    overflowY: 'auto',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: 1.5,
                  }}
                >
                  {filteredTickets.map((ticket) => (
                    <Card
                      key={ticket.id}
                      elevation={1}
                      onClick={() => router.push(`/kanban/${boardId}/ticket/${ticket.id}`)}
                      sx={{
                        borderRadius: 1.5,
                        transition: 'box-shadow 0.2s',
                        '&:hover': { boxShadow: 3 },
                      }}
                    >
                      <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1 }}>
                          <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 'bold' }}>
                            {ticket.formatted_number}
                          </Typography>
                          
                          <IconButton
                            size="small"
                            onClick={() => openMoveModal(ticket)}
                            title="Mover de coluna"
                            sx={{ p: 0.5 }}
                          >
                            <MoveIcon fontSize="small" color="action" />
                          </IconButton>
                        </Box>

                        <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 'bold' }}>
                          {ticket.title}
                        </Typography>

                        {ticket.description && (
                          <Typography
                            variant="body2"
                            color="text.secondary"
                            sx={{
                              mb: 1.5,
                              display: '-webkit-box',
                              WebkitLineClamp: 2,
                              WebkitBoxOrient: 'vertical',
                              overflow: 'hidden',
                            }}
                          >
                            {ticket.description}
                          </Typography>
                        )}

                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 1 }}>
                          {ticket.due_date ? (
                            <Chip
                              icon={<CalendarIcon style={{ fontSize: 14 }} />}
                              label={new Date(ticket.due_date).toLocaleDateString('pt-BR')}
                              size="small"
                              variant="outlined"
                              sx={{ fontSize: '0.7rem' }}
                            />
                          ) : (
                            <Box />
                          )}

                          <Avatar sx={{ width: 24, height: 24, fontSize: '0.75rem', bgcolor: 'primary.light' }}>
                            {ticket.owner}
                          </Avatar>
                        </Box>
                      </CardContent>
                    </Card>
                  ))}

                  {filteredTickets.length === 0 && (
                    <Typography variant="caption" color="text.secondary" sx={{ py: 3, fontStyle: 'italic', textAlign: 'center' }}>
                      Nenhuma tarefa nesta coluna.
                    </Typography>
                  )}
                </Box>
              </Paper>
            );
          })
        )}
      </Box>

      <Dialog open={isCreateModalOpen} onClose={() => setIsCreateModalOpen(false)} fullWidth maxWidth="xs">
        <DialogTitle sx={{ fontWeight: 'bold' }}>Nova Tarefa</DialogTitle>
        <Box component="form" onSubmit={handleCreateTicket}>
          <DialogContent dividers sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <FormControl fullWidth size="small" required>
              <InputLabel>Coluna</InputLabel>
              <Select
                value={selectedColumnId}
                label="Coluna"
                onChange={(e) => setSelectedColumnId(Number(e.target.value))}
              >
                {board?.columns?.map((col) => (
                  <MenuItem key={col.id} value={col.id}>
                    {col.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <TextField
              label="Título"
              required
              fullWidth
              size="small"
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
            />

            <TextField
              label="Descrição"
              multiline
              rows={3}
              fullWidth
              size="small"
              value={newDescription}
              onChange={(e) => setNewDescription(e.target.value)}
            />

            <TextField
              label="Data de Vencimento"
              type="date"
              fullWidth
              size="small"
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
            <Button onClick={() => setIsCreateModalOpen(false)} color="inherit" disabled={isSubmitting}>
              Cancelar
            </Button>
            <Button type="submit" variant="contained" color="primary" disabled={isSubmitting}>
              {isSubmitting ? 'Salvando...' : 'Criar Tarefa'}
            </Button>
          </DialogActions>
        </Box>
      </Dialog>

      <Dialog open={isMoveModalOpen} onClose={() => setIsMoveModalOpen(false)} fullWidth maxWidth="xs">
        <DialogTitle sx={{ fontWeight: 'bold' }}>Mover Tarefa</DialogTitle>
        <Box component="form" onSubmit={handleMoveTicket}>
          <DialogContent dividers sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Typography variant="body2" color="text.secondary">
              Mover <strong>{ticketToMove?.formatted_number} - {ticketToMove?.title}</strong> para a coluna:
            </Typography>

            <FormControl fullWidth size="small" required>
              <InputLabel>Nova Coluna</InputLabel>
              <Select
                value={targetColumnId}
                label="Nova Coluna"
                onChange={(e) => setTargetColumnId(Number(e.target.value))}
              >
                {board?.columns?.map((col) => (
                  <MenuItem key={col.id} value={col.id}>
                    {col.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </DialogContent>
          <DialogActions sx={{ p: 2 }}>
            <Button onClick={() => setIsMoveModalOpen(false)} color="inherit" disabled={isSubmitting}>
              Cancelar
            </Button>
            <Button type="submit" variant="contained" color="primary" disabled={isSubmitting}>
              {isSubmitting ? 'Salvando...' : 'Mover'}
            </Button>
          </DialogActions>
        </Box>
      </Dialog>
    </Box>
  );
}