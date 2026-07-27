'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import {
  Box,
  Typography,
  Button,
  Container,
  Card,
  CardContent,
  CardActionArea,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  InputAdornment,
  Pagination,
  CircularProgress,
  Alert,
} from '@mui/material';
import Grid from '@mui/material/Grid';
import {
  Add as AddIcon,
  Search as SearchIcon,
  ExitToApp as LogoutIcon,
  Dashboard as DashboardIcon,
  ViewColumn as ViewColumnIcon,
} from '@mui/icons-material';
import Cookies from 'js-cookie';
import api from '@/services/api';
import logoImg from '@/assets/logo.png';
import Header from '@/components/Header';

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

export interface Board {
  id: number;
  name: string;
  description: string;
  color: string;
  owner: number;
  columns: Column[];
  created_at: string;
  updated_at: string;
}

interface PaginatedApiResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export default function BoardsPage() {
  const router = useRouter();

  const [boards, setBoards] = useState<Board[]>([]);
  const [totalCount, setTotalCount] = useState(0);
  const [page, setPage] = useState(1);
  const PAGE_SIZE = 10;

  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newBoardName, setNewBoardName] = useState('');
  const [newBoardDesc, setNewBoardDesc] = useState('');
  const [newBoardColor, setNewBoardColor] = useState('#3B82F6');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const fetchBoards = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get<PaginatedApiResponse<Board>>('/tickets/board/', {
        params: {
          page: page,
          search: searchTerm || undefined,
        },
      });

      setBoards(response.data.results);
      setTotalCount(response.data.count);
    } catch (err: any) {
      setError('Não foi possível carregar os quadros.');
    } finally {
      setLoading(false);
    }
  }, [page, searchTerm]);

  useEffect(() => {
    fetchBoards();
  }, [fetchBoards]);

  const handleLogout = () => {
    Cookies.remove('access_token');
    Cookies.remove('refresh_token');
    router.push('/login');
  };

  const handleCreateBoard = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newBoardName.trim()) return;

    setIsSubmitting(true);
    try {
      await api.post('/tickets/board/', {
        name: newBoardName,
        description: newBoardDesc,
        color: newBoardColor,
      });

      setIsModalOpen(false);
      setNewBoardName('');
      setNewBoardDesc('');
      setNewBoardColor('#3B82F6');
      
      setPage(1);
      fetchBoards();
    } catch (err: any) {
      console.error('Erro ao criar quadro:', err);
      alert('Erro ao criar o quadro. Verifique os dados.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const getTotalTickets = (board: Board): number => {
    return board.columns?.reduce((acc, col) => acc + (col.tickets?.length || 0), 0) || 0;
  };

  const formatDate = (isoString: string) => {
    if (!isoString) return '';
    return new Date(isoString).toLocaleDateString('pt-BR');
  };

  const totalPages = Math.ceil(totalCount / PAGE_SIZE);

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default', display: 'flex', flexDirection: 'column' }}>
      <Header title='Meus Quadros' />

      <Container maxWidth="lg" sx={{ py: 4, flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4, flexWrap: 'wrap', gap: 2 }}>
          <TextField
            placeholder="Buscar quadro..."
            size="small"
            value={searchTerm}
            onChange={(e) => {
              setSearchTerm(e.target.value);
              setPage(1);
            }}
            sx={{ width: { xs: '100%', sm: 350 } }}
            slotProps={{
              input: {
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon color="action" />
                  </InputAdornment>
                ),
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
            Novo Quadro
          </Button>
        </Box>

        {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', my: 8 }}>
            <CircularProgress />
          </Box>
        ) : (
          <>
            <Grid container spacing={3} sx={{ flexGrow: 1 }}>
              {boards.map((board) => (
                <Grid key={board.id} size={{ xs: 12, sm: 6, md: 4 }}>
                  <Card
                    elevation={2}
                    sx={{
                      borderRadius: 3,
                      height: '100%',
                      display: 'flex',
                      flexDirection: 'column',
                      borderLeft: `6px solid ${board.color || '#3B82F6'}`,
                      transition: 'transform 0.2s, box-shadow 0.2s',
                      '&:hover': {
                        transform: 'translateY(-4px)',
                        boxShadow: 6,
                      },
                    }}
                  >
                    <CardActionArea
                      onClick={() => router.push(`/kanban/${board.id}`)}
                      sx={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'stretch', justifyContent: 'space-between' }}
                    >
                      <CardContent>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                          <DashboardIcon sx={{ color: board.color || 'primary.main' }} fontSize="small" />
                          <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                            {board.name}
                          </Typography>
                        </Box>

                        <Typography variant="body2" color="text.secondary" sx={{ mb: 2, minHeight: 40 }}>
                          {board.description || 'Sem descrição cadastrada.'}
                        </Typography>

                        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                          <Chip
                            icon={<ViewColumnIcon />}
                            label={`${board.columns?.length || 0} colunas`}
                            size="small"
                            variant="outlined"
                          />
                          <Chip
                            label={`${getTotalTickets(board)} tarefas`}
                            size="small"
                            variant="outlined"
                            color="primary"
                          />
                        </Box>
                      </CardContent>

                      <Box sx={{ px: 2, pb: 2, display: 'flex', justifyContent: 'space-between', borderTop: 1, borderColor: 'divider', pt: 1.5 }}>
                        <Typography variant="caption" color="text.secondary">
                          Criado: {formatDate(board.created_at)}
                        </Typography>
                        <Typography variant="caption" color="primary" sx={{ fontWeight: 'bold' }}>
                          Abrir Quadro →
                        </Typography>
                      </Box>
                    </CardActionArea>
                  </Card>
                </Grid>
              ))}

              {boards.length === 0 && (
                <Grid size={{ xs: 12 }}>
                  <Box sx={{ textAlign: 'center', py: 8 }}>
                    <Typography color="text.secondary">
                      Nenhum quadro encontrado.
                    </Typography>
                  </Box>
                </Grid>
              )}
            </Grid>

            {/* Paginação ligada no DRF */}
            {totalPages > 1 && (
              <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
                <Pagination
                  count={totalPages}
                  page={page}
                  onChange={(_, value) => setPage(value)}
                  color="primary"
                  shape="rounded"
                />
              </Box>
            )}
          </>
        )}
      </Container>

      <Dialog open={isModalOpen} onClose={() => setIsModalOpen(false)} fullWidth maxWidth="xs">
        <DialogTitle sx={{ fontWeight: 'bold' }}>Criar Novo Quadro</DialogTitle>
        <Box component="form" onSubmit={handleCreateBoard}>
          <DialogContent dividers sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              label="Nome do Quadro"
              required
              fullWidth
              value={newBoardName}
              onChange={(e) => setNewBoardName(e.target.value)}
            />
            <TextField
              label="Descrição"
              multiline
              rows={3}
              fullWidth
              value={newBoardDesc}
              onChange={(e) => setNewBoardDesc(e.target.value)}
            />
            <TextField
              label="Cor (Hexadecimal)"
              type="color"
              fullWidth
              value={newBoardColor}
              onChange={(e) => setNewBoardColor(e.target.value)}
              sx={{ '& input': { height: 40, cursor: 'pointer' } }}
            />
          </DialogContent>
          <DialogActions sx={{ p: 2 }}>
            <Button onClick={() => setIsModalOpen(false)} color="inherit" disabled={isSubmitting}>
              Cancelar
            </Button>
            <Button type="submit" variant="contained" color="primary" disabled={isSubmitting}>
              {isSubmitting ? 'Criando...' : 'Criar'}
            </Button>
          </DialogActions>
        </Box>
      </Dialog>
    </Box>
  );
}
