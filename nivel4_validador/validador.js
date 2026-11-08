// NÍVEL 4 — Torre do Validador (Node: JavaScript)
//
// Você vai montar o validador de um formulário de cadastro com FÁBRICAS de regras (closures)
// e depois COMPOR essas regras. Siga as missões na ordem e rode:  python quest.py 4   (veja o LEIAME.md).
//
// Quer usar TypeScript? Apague este arquivo (validador.js) e implemente o validador.ts.
//
// Um VALIDADOR é uma função (valor) => null   (se está tudo certo)
//                              ou (valor) => "mensagem de erro".
// Uma FÁBRICA é uma função que devolve um validador, "lembrando" os parâmetros que recebeu (closure).

// ============================================================ MISSÃO 4.1 — Fábricas de regras (closures)
/** obrigatorio("Nome") devolve um validador: valor vazio, só com espaços, null ou undefined
 *  => "Nome é obrigatório"; caso contrário null. */
export function obrigatorio(campo) {
  return (valor) => (String(valor ?? "").trim() ? null : `${campo} é obrigatório`);
}

/** minimo("Senha", 8) devolve um validador: menos de 8 caracteres => "Senha deve ter pelo menos 8 caracteres". */
export function minimo(campo, n) {
  return (valor) =>
    String(valor ?? "").length < n ? `${campo} deve ter pelo menos ${n} caracteres` : null;
}

/** padrao("E-mail", /@/, "conter @") devolve um validador: se o texto não casa com a regex => "E-mail deve conter @".
 *  Dica: regex.test(String(valor ?? "")) */
export function padrao(campo, regex, descricao) {
  return (valor) =>
    new RegExp(regex.source, regex.flags).test(String(valor ?? ""))
      ? null
      : `${campo} deve ${descricao}`;
}

// ============================================================ MISSÃO 4.2 — Compondo regras
/** todas(v1, v2, ...) devolve um validador que roda os validadores em ordem e devolve o PRIMEIRO erro (ou null). */
export function todas(...validadores) {
  return (valor) => validadores.map((validar) => validar(valor)).find((erro) => erro !== null) ?? null;
}

/** acumular(v1, v2, ...) devolve um validador que devolve a LISTA de todos os erros ([] se estiver tudo certo). */
export function acumular(...validadores) {
  return (valor) => validadores.map((validar) => validar(valor)).filter((erro) => erro !== null);
}

// ============================================================ MISSÃO 4.3 — O formulário completo
/** regras: { campo: validador }. dados: { campo: valor }.
 *  Devolve { valido: boolean, erros: { campo: "primeira mensagem" } } só com os campos que falharam.
 *  Dica: Object.entries, map, filter, Object.fromEntries. Não altere regras nem dados! */
export function validarFormulario(regras, dados) {
  const erros = Object.fromEntries(
    Object.entries(regras)
      .map(([campo, validar]) => [campo, validar(dados[campo])])
      .filter(([, erro]) => erro !== null),
  );
  return { valido: Object.keys(erros).length === 0, erros };
}
