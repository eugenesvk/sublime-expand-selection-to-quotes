import sublime, sublime_plugin

from . import cfg

import logging
DEFAULT_LOG_LEVEL = logging.WARNING
_log = logging.getLogger(__name__)
_log.setLevel(DEFAULT_LOG_LEVEL)
_L = False #dbg

class ExpandSelectionToQuotesCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		C = cfg.cfgU.C
		view = self.view

		q_pt_all = {}
		for q in C['q=']: # " ' `
			q_pt_all[q] = list(map(lambda x: x.begin(), view.find_all(q)))

		def search_for_quotes(q, q_pts, txt_pt):
			q_size, before, after = False, False, False
			if len(q_pts) - view.substr(sel).count('"') < 2: # not enough pairs
				return q_size, before, after

			# 1. Limit quotes to a string
			txt_scope = view.scope_name(txt_pt) #e.g., "source.python meta.function…"

			str_scope = None
			for  i_str in C['str']:
				if i_str in txt_scope: # found partial 'meta.string', find full '….python'
					for  i_txt in reversed(txt_scope.split()): # guard: search for most specific match first
						if i_txt.startswith(i_str):
							str_scope = i_txt
							break
			all_before, all_after = None, None

			if str_scope:
				if (s := view.expand_to_scope(txt_pt, str_scope)):
					all_before = list(filter(lambda x: (x <  sel.begin()) \
					  and                              (x >=   s.begin()), q_pts))
					all_after  = list(filter(lambda x: (x >= sel.end  ()) \
					  and                              (x <=   s.end  ()), q_pts))
			else:
				all_before   = list(filter(lambda x:  x <  sel.begin() , q_pts))
				all_after    = list(filter(lambda x:  x >= sel.end  () , q_pts))

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
							continue
					if is_esc: continue
					after = i_q
					if     _L: _log.debug(f'✓POS {q} @ {i_q} of {ctx_q}')
					break
			if before is not None and after is not None: q_size = after - before

			return q_size, before, after

		def replace_region(start, end):
			if sel.size() < end-start-2:
				start += 1; end -= 1
			view.sel().subtract(sel)
			view.sel().add(sublime.Region(start, end))

		for sel in view.sel():
			txt_pt = sel.b # ignore selection, only use point @ ⎀

			q_res = {}
			for q in C['q=']: # " ' `             ↓list[sublime.Point]
				sz, pre, pos = search_for_quotes(q, q_pt_all[q], txt_pt)
				q_res[sz] = (pre,pos)
				if _L: _log.debug(f"q={q} pre={pre} pos={pos} q_pt={q_pt_all[q]}")

			min_sz = None
			for sz in q_res: # find the nearest quotes…
				if sz:
					if not min_sz:
						min_sz =     sz
					else:
						min_sz = min(sz, min_sz)
			if min_sz:      # …use their region for selection
				replace_region(q_res[min_sz][0], q_res[min_sz][1] + 1)
			if _L: _log.debug(f"min_sz={min_sz}")
