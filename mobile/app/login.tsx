import { useState } from "react";
import { View, Text, TextInput, Pressable, StyleSheet, Alert } from "react-native";
import { router } from "expo-router";
import { login } from "../services/api";

export default function Login() {
  const [username,setUsername]=useState("");
  const [password,setPassword]=useState("");
  const [busy,setBusy]=useState(false);

  async function submit(){
    try{
      setBusy(true);
      await login(username,password);
      router.replace("/dashboard");
    }catch(e){ Alert.alert("Connexion", e instanceof Error ? e.message : "Erreur"); }
    finally{ setBusy(false); }
  }

  return <View style={s.page}>
    <Text style={s.brand}>MG ASSISTANCE</Text>
    <Text style={s.title}>Bienvenue sur MGA Mobile</Text>
    <Text style={s.sub}>Gestion commerciale et technique</Text>
    <TextInput style={s.input} placeholder="Nom d'utilisateur" autoCapitalize="none" value={username} onChangeText={setUsername}/>
    <TextInput style={s.input} placeholder="Mot de passe" secureTextEntry value={password} onChangeText={setPassword}/>
    <Pressable style={s.button} onPress={submit} disabled={busy}><Text style={s.bt}>{busy?"Connexion…":"Se connecter"}</Text></Pressable>
  </View>;
}
const s=StyleSheet.create({
  page:{flex:1,justifyContent:"center",padding:24,backgroundColor:"#fff"},
  brand:{fontSize:26,fontWeight:"800",color:"#08783e",marginBottom:28},
  title:{fontSize:24,fontWeight:"700"}, sub:{marginTop:6,marginBottom:28,color:"#667085"},
  input:{borderWidth:1,borderColor:"#D0D5DD",borderRadius:12,padding:15,marginBottom:12},
  button:{backgroundColor:"#08783e",padding:16,borderRadius:12,alignItems:"center",marginTop:8},
  bt:{color:"#fff",fontWeight:"700"}
});
