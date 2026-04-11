import sublime, sublime_plugin

from . import cfg

import logging
DEFAULT_LOG_LEVEL = logging.WARNING
_log = logging.getLogger(__name__)
_log.setLevel(DEFAULT_LOG_LEVEL)
_L = False #dbg

class ExpandSelectionToQuotesCommand(sublime_plugin.TextCommand):
  def run(self, edit, qp=False, inc=False): # ↓ enable soft-undo
    sublime.set_timeout(lambda: self.view.run_command('expand_selection_to_quotes_atomic',
      {"qp":qp, "inc": inc}),
      0) # delay

class ExpandSelectionToQuotesAtomicCommand(sublime_plugin.TextCommand):
  def run(self, edit, qp=False, inc=False):
    C = cfg.cfgU.C
    view = self.view
    flit = sublime.FindFlags.LITERAL

    q_pt_all = {}
    for q in C['q=']: # " ' `
      q_pt_all[q] = list(map(lambda x: x.begin(), view.find_all(q   ,flit)))
    if qp:
      for q in C['qp']: # «»  “”
        q_lbl = q if type(q) is str else ''.join(q)
        q_pt_all[q_lbl] = {
          'beg'   : list(map(lambda x: x.begin(), view.find_all(q[0],flit))),
          'end'   : list(map(lambda x: x.begin(), view.find_all(q[1],flit))),
        }

    def search_for_quotes(q, q_pts, txt_pt, is_p=False):
      q_size, before,after = False, False, False
      q0     =     q[0] if is_p else q; q1     =     q[1] if is_p else q
      ql_pre = len(q0)                ; ql_pos = len(q1)
      q_pts_beg = q_pts['beg'] if is_p else q_pts
      q_pts_end = q_pts['end'] if is_p else q_pts
      count_q  = len(q_pts_beg) + (len(q_pts_end) if is_p else 0)
      count_qq = 0 # number of quotes within the selection
      if q0 == q1:
        count_qq = view.substr(sel).count(q0)
      else:
        sel_s = view.substr(sel)
        q0_cnt = sel_s.count(q0);  q1_cnt = sel_s.count(q1)
        if q1 in q0: q1_cnt -= q0_cnt  #`'  '  then matching q1' counted all q0`'
        if q0 in q1: q0_cnt -= q1_cnt  # ' `'  then matching q0' counted all q1`'
        count_qq = q0_cnt + q1_cnt
      if count_q - count_qq < 2: # not enough pairs
        return q_size, before,after,  ql_pre,ql_pos

      # 1. Limit quotes to a string
      txt_scope = view.scope_name(txt_pt) #e.g., "source.python meta.function…"

      str_scope = None # Find string scope to avoid jumping outside of it
      for  i_str in C['str']:
        if str_scope: break
        if i_str in txt_scope: # found partial 'meta.string', find full '….python'
          for  i_txt in reversed(txt_scope.split()): # guard: search for most specific match first
            if i_txt.startswith(i_str):
              str_scope = i_txt
              break
      cmt_scope = None # Find comment scope to avoid jumping outside of it
      for  i_cmt in C['cmt']:
        if cmt_scope: break
        if i_cmt in txt_scope: # found partial 'comment.line', find full '….number-sign.python'
          for  i_txt in reversed(txt_scope.split()): # guard: search for most specific match first
            if i_txt.startswith(i_cmt):
              cmt_scope = i_txt
              break
      src_scope = None # Find source scope to avoid jumping outside of it
      i_src = 'source.'
      if i_src in txt_scope: # found partial 'source.', find full '….python'
        for  i_txt in reversed(txt_scope.split()): # guard: search for most specific match first
          if i_txt.startswith(i_src):
            src_scope = i_txt
            break
      all_before, all_after = None, None

      lim, is_src, is_str, is_cmt = None, None, None, None
      if  src_scope and (reg_src := view.expand_to_scope(txt_pt, src_scope)): is_src = True
      if  str_scope and (reg_str := view.expand_to_scope(txt_pt, str_scope)): is_str = True
      if  cmt_scope and (reg_cmt := view.expand_to_scope(txt_pt, cmt_scope)): is_cmt = True
      if is_src: lim =                  reg_src
      if is_str: lim = lim.intersection(reg_str) if lim else reg_str
      if is_cmt: lim = lim.intersection(reg_cmt) if lim else reg_cmt
      if _L: _log.debug(f"{'✓'if is_src else '✗'}src={src_scope}  {'✓'if is_str else '✗'}str={str_scope} {'✓'if is_cmt else '✗'}cmt={cmt_scope} lim={lim}")

      if lim:
        all_before = list(filter(lambda x: (x <  sel.begin()) \
          and                              (x >= lim.begin()), q_pts_beg))
        all_after  = list(filter(lambda x: (x >= sel.end  ()) \
          and                              (x <= lim.end  ()), q_pts_end))
      else:
        all_before = list(filter(lambda x:  x <  sel.begin() , q_pts_beg))
        all_after  = list(filter(lambda x:  x >= sel.end  () , q_pts_end))
      if _L: _log.debug(f"all_before = {all_before}\nall_after = {all_after}  sel={sel.end()} s={s.end()} q_pts_end={q_pts_end}  q_pt_all={q_pt_all}")

      # 2. Find quotes that do/are not escape(s)
      esc   = C['esc'] # constant.character.escape
      before, after = None, None
      if all_before: # Find the first unescaped quote
        for  i_q in reversed(all_before):
          is_esc = False
          ctx_q = view.scope_name(i_q) #e.g., "… constant.character.escape …"
          for  s in esc:
            if s and s in ctx_q: # guards against empty scopes
              is_esc = True
              if _L: _log.debug(f"⎋PRE {q} @ {i_q} of {s} in {ctx_q}")
              break
          if is_esc: continue
          before = i_q
          if     _L: _log.debug(f'✓PRE {q} @ {i_q} of {ctx_q}')
          break
      if all_after : # Find the last unescaped quote
        for  i_q in          all_after  :
          is_esc = False
          ctx_q = view.scope_name(i_q) #e.g., "… constant.character.escape …"
          for  s in esc:
            if s and s in ctx_q: # guards against empty scopes
              is_esc = True
              if _L: _log.debug(f"⎋POS {q} @ {i_q} of {s} in {ctx_q}")
              break
          if is_esc: continue
          after = i_q
          if     _L: _log.debug(f'✓POS {q} @ {i_q} of {ctx_q}')
          break
      if before is not None and after is not None: q_size = after - (before + ql_pre)

      return q_size, before,after,  ql_pre,ql_pos

    def replace_region(start, end, pre_ql,pos_ql):
      if sel.size() < end - start - pre_ql - 1:
        start += pre_ql; end -= 1
      else:
        end   += pos_ql - 1
      view.sel().subtract(sel)
      view.sel().add(sublime.Region(start, end))

    for sel in view.sel():
      txt_pt = sel.b # ignore selection, only use point @ ⎀

      q_res = {}
      for q in C['q=']: # " ' `             ↓list[sublime.Point]
        sz, pre,pos,  ql_pre,ql_pos = search_for_quotes(q, q_pt_all[q], txt_pt, is_p=False)
        q_res[sz] = (pre,pos,  ql_pre,ql_pos)
        if _L: _log.debug(f"q={q} pre={pre} pos={pos} q_pt={q_pt_all[q]}")
      if qp:
        for q in C['qp']: # «»  “”
          q_lbl = q if type(q) is str else ''.join(q)
          sz, pre,pos,  ql_pre,ql_pos = search_for_quotes(q, q_pt_all[q_lbl], txt_pt, is_p=True)
          q_res[sz] = (pre,pos,  ql_pre,ql_pos)
          if _L: _log.debug(f"q={q} pre={pre} pos={pos} q_pt={q_pt_all[q_lbl]} sz={sz}¦{ql_pre}¦{ql_pos}")

      min_sz = None
      for sz in q_res: # find the nearest quotes…
        if sz:
          if not min_sz:
            min_sz =     sz
          else:
            min_sz = min(sz, min_sz)
      if min_sz:      # …use their region for selection
        pre_t , pos_t  = q_res[min_sz][0], q_res[min_sz][1]
        pre_ql, pos_ql = q_res[min_sz][2], q_res[min_sz][3]
        beg = pre_t     - (pre_ql if inc else 0)
        end = pos_t + 1 + (pos_ql if inc else 0)
        replace_region(beg, end, pre_ql,pos_ql)
      if _L: _log.debug(f"min_sz={min_sz}")
  def search_for_scope(self, scope_nm, txt_pt):
    """Returns a range matching the scope and a pair of regions matching opening/closing quotes
    """
    C = cfg.cfgU.C
    view = self.view

    reg_str_full, reg_str_b, reg_str_e = None, None, None
    scope_l = scope_nm if type(scope_nm) is list else [scope_nm]

    txt_scope = view.scope_name(txt_pt) #e.g., "source.python meta.string…"

    str_scope = None # Find string scope to expand to it (exclude open/close marks later)
    for i_str in scope_l:
      if i_str in txt_scope: # found partial 'string.', find full '….python'
        for  i_txt in reversed(txt_scope.split()): # guard: search for most specific match first
          if i_txt.startswith(i_str):
            str_scope = i_txt
            break
    if str_scope and (reg_str_full := view.expand_to_scope(txt_pt, str_scope)):
      str_b0 = reg_str_full.begin(); txt_sc_b0 = view.scope_name(str_b0)
      str_e0 = reg_str_full.end  ();
      if str_e0 > str_b0:
        str_e0 -= 1
      txt_sc_e0                                = view.scope_name(str_e0)

      str_scope_b, str_scope_e = None, None
      for i_str in C['str_b']: # partial scope names
        for  i_txt in reversed(txt_sc_b0.split()): # guard: search for most specific match first
          if i_txt.startswith(i_str):
            reg_str_b = view.expand_to_scope(str_b0, i_txt)
            break
      for i_str in C['str_e']:
        for  i_txt in reversed(txt_sc_e0.split()):
          if i_txt.startswith(i_str):
            reg_str_e = view.expand_to_scope(str_e0, i_txt)
            break

    return reg_str_full, (reg_str_b, reg_str_e)
