"use client";

import Image from "next/image";
import { useRouter } from 'next/navigation';

import Cookies from 'js-cookie';

import { AppBar, Avatar, Box, Button, Toolbar, Typography } from "@mui/material";
import { ExitToApp as LogoutIcon,} from '@mui/icons-material';

import logoImg from '@/assets/logo.png';


export default function Header() {
  const router = useRouter();

  const handleLogout = () => {
    Cookies.remove('access_token');
    Cookies.remove('refresh_token');
    router.push('/login');
  };

  return (
    <AppBar position="static" color="inherit" elevation={1} sx={{ borderBottom: 1, borderColor: 'divider' }}>
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Image src={logoImg} alt="Kanban Logo" width={60} height={40} style={{ objectFit: 'contain' }} />
          <Typography variant="h6" sx={{ fontWeight: 'medium' }}>
            Desenvolvimento
          </Typography>
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Avatar sx={{ bgcolor: 'primary.main', width: 32, height: 32 }}>U</Avatar>
            <Typography variant="body2" sx={{ fontWeight: 'medium'}}>
              Usuário
            </Typography>
          </Box>

          <Button
            variant="outlined"
            color="error"
            size="small"
            startIcon={<LogoutIcon />}
            onClick={handleLogout}
          >
            Sair
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
}