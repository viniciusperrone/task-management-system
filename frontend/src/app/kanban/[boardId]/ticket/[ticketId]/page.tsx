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
  Container,
  Paper,
  Grid,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  OutlinedInput,
  Chip,
  Avatar,
  Divider,
  CircularProgress,
  Alert,
  Snackbar,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Save as SaveIcon,
  People as PeopleIcon,
  ExitToApp as LogoutIcon,
} from '@mui/icons-material';
import api from '@/services/api';
import { useAuth } from '@/context/AuthContext';
import logoImg from '@/assets/logo.png';
import Header from '@/components/Header';

export interface UserOption {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

export interface TicketDetail {
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

export default function TicketDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { user, logout } = useAuth();

  const boardId = params.boardId as string;
  const ticketId = params.ticketId as string;

  const [ticket, setTicket] = useState<TicketDetail | null>(null);
  const [usersList, setUsersList] = useState<UserOption[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState(false);

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<number>(30);
  const [dueDate, setDueDate] = useState<string>('');
  const [selectedSharedUsers, setSelectedSharedUsers] = useState<number[]>([]);

  const fetchData = useCallback(async () => {
    if (!ticketId) return;
    setLoading(true);
    setError(null);
    try {
      const ticketRes = await api.get<TicketDetail>(`/tickets/ticket/${ticketId}/`);
      const ticketData = ticketRes.data;

      setTicket(ticketData);
      setTitle(ticketData.title || '');
      setDescription(ticketData.description || '');
      setPriority(ticketData.priority || 30);
      setDueDate(ticketData.due_date || '');
      setSelectedSharedUsers(ticketData.shared_users || []);

      try {
        const usersRes = await api.get<UserOption[]>('/iam/users/');
        setUsersList(usersRes.data);
      } catch (userErr) {
        console.warn('Não foi possível carregar a lista de usuários:', userErr);
      }
    } catch (err: any) {
      console.error('Erro ao carregar detalhes do ticket:', err);
      setError('Não foi possível carregar as informações deste ticket.');
    } finally {
      setLoading(false);
    }
  }, [ticketId]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await api.patch(`/tickets/ticket/${ticketId}/`, {
        title,
        description,
        priority: Number(priority),
        due_date: dueDate || null,
        shared_users: selectedSharedUsers,
      });

      setSuccessMessage(true);
    } catch (err) {
      console.error('Erro ao atualizar ticket:', err);
      alert('Não foi possível salvar as alterações do ticket.');
    } finally {
      setSaving(false);
    }
  };

  const userDisplayName = user
    ? user.first_name ? `${user.first_name} ${user.last_name}`.trim() : user.username
    : 'Usuário';

  const avatarInitial = userDisplayName[0]?.toUpperCase() || 'U';

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default', display: 'flex', flexDirection: 'column' }}>
      <Header title={ticket?.title || 'Carregando...'}/>

      <Container maxWidth="md" sx={{ py: 4, flexGrow: 1 }}>
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', my: 8 }}>
            <CircularProgress />
          </Box>
        ) : error ? (
          <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>
        ) : (
          <Paper elevation={2} sx={{ p: 4, borderRadius: 3 }}>
            <Box component="form" onSubmit={handleSave}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
                  <Chip
                    label={ticket?.formatted_number}
                    color="primary"
                    sx={{ fontWeight: 'bold' }}
                  />
                  <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
                    Detalhes da Tarefa
                  </Typography>
                </Box>

                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  startIcon={<SaveIcon />}
                  disabled={saving}
                >
                  {saving ? 'Salvando...' : 'Salvar Alterações'}
                </Button>
              </Box>

              <Divider sx={{ mb: 4 }} />

              <Grid container spacing={3}>
                <Grid size={{ xs: 12 }}>
                  <TextField
                    label="Título da Tarefa"
                    required
                    fullWidth
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                  />
                </Grid>

                <Grid size={{ xs: 12 }}>
                  <TextField
                    label="Descrição Detalhada"
                    multiline
                    rows={5}
                    fullWidth
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                  />
                </Grid>

                <Grid size={{ xs: 12, sm: 6 }}>
                  <TextField
                    label="Prioridade"
                    type="number"
                    fullWidth
                    value={priority}
                    onChange={(e) => setPriority(Number(e.target.value))}
                  />
                </Grid>

                <Grid size={{ xs: 12, sm: 6 }}>
                  <TextField
                    label="Data de Vencimento"
                    type="date"
                    fullWidth
                    slotProps={{ 
                      inputLabel: {
                        shrink: true
                      }
                    }}
                    value={dueDate}
                    onChange={(e) => setDueDate(e.target.value)}
                  />
                </Grid>

                <Grid size={{ xs: 12 }}>
                  <Box sx={{ p: 2.5, border: '1px solid', borderColor: 'divider', borderRadius: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                      <PeopleIcon color="primary" />
                      <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                        Compartilhar com outros Usuários
                      </Typography>
                    </Box>

                    <FormControl fullWidth size="small">
                      <InputLabel id="shared-users-label">Selecione os Usuários</InputLabel>
                      <Select
                        labelId="shared-users-label"
                        multiple
                        value={selectedSharedUsers}
                        onChange={(e) => {
                          const value = e.target.value;
                          setSelectedSharedUsers(
                            typeof value === 'string' ? value.split(',').map(Number) : value
                          );
                        }}
                        input={<OutlinedInput label="Selecione os Usuários" />}
                        renderValue={(selected) => (
                          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                            {selected.map((userId) => {
                              const foundUser = usersList?.find((u) => u.id === userId);
                              return (
                                <Chip
                                  key={userId}
                                  label={foundUser ? `${foundUser.first_name || foundUser.username}` : `Usuário #${userId}`}
                                  size="small"
                                />
                              );
                            })}
                          </Box>
                        )}
                      >
                        {usersList.map((u) => (
                          <MenuItem key={u.id} value={u.id}>
                            {u.first_name ? `${u.first_name} ${u.last_name} (${u.username})` : u.username}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  </Box>
                </Grid>
              </Grid>
            </Box>
          </Paper>
        )}
      </Container>

      <Snackbar
        open={successMessage}
        autoHideDuration={3000}
        onClose={() => setSuccessMessage(false)}
        message="Ticket atualizado com sucesso!"
      />
    </Box>
  );
}