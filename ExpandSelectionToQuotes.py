import sublime, sublime_plugin

from . import cfg
import logging
DEFAULT_LOG_LEVEL = logging.WARNING
_log = logging.getLogger(__name__)
_log.setLevel(DEFAULT_LOG_LEVEL)
_L = False #dbg

class ExpandSelectionToQuotesCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		q_all = {}
		for q in self.q_same:
			q_all[q] = list(map(lambda x: x.begin(), self.view.find_all(q)))

		def search_for_quotes(q, quotes, esc, esc_self):
			q_size, before, after = False, False, False

			if len(quotes) - self.view.substr(sel).count('"') >= 2:
				all_before = list(filter(lambda x: x <  sel.begin(), quotes))
				all_after  = list(filter(lambda x: x >= sel.end  (), quotes))
				before, after = None, None
				esc_c = esc['c'  ] # {c: \    sym: " '}
				is_esc = True if q == esc_c else False # single quote can act as an escape

				if all_before: # Find escaped quotes and skip them
					for  i_q in reversed(all_before):
						if is_esc: # check if this is an escape for the next char `', not a standalone quote `
							char_pos_q = None if (i_q + 1) >= self.view.__len__() else self.view.substr(i_q + 1)
							if char_pos_q and char_pos_q in esc['sym']: # not a quote, but an escape
								continue
						if i_q == 0: # ␂, so don't check for escape char before this
							before = i_q
							if _L: _log.debug(f'✓PRE {q} @ {before} a.k.a. ␂')
							break
						else:
							char_pre_q = self.view.substr(i_q - 1)
							if   char_pre_q == esc_c:
								if _L: _log.debug(f"{esc_c}PRE q={q} @ {i_q} pre_char=¦{char_pre_q}¦")
								continue
							elif char_pre_q == q and q in esc_self:
								if _L: _log.debug(f"••{esc_c}PRE q={q} @ {i_q} pre_char=¦{char_pre_q}¦")
								continue
							else:
								before = i_q
								if _L: _log.debug(f'✓PRE {q} @ {before} with pre_char=¦{char_pre_q}¦')
								break
				if all_after:
					skip_paired = False
					for  i_q in          all_after  :
						if is_esc: # check if this is an escape for the next char `', not a standalone quote `
							char_pos_q = None if (i_q + 1) >= self.view.__len__() else self.view.substr(i_q + 1)
							if char_pos_q and char_pos_q in esc['sym']: # not a quote, but an escape
								continue

						if skip_paired:
							skip_paired = False
							if _L: _log.debug(f"••₂{esc_c}POS q={q} @ {i_q} & {esc_self}")
							continue

						if i_q == 0: # shouldn't happen, but just in case
							after = i_q
							if _L: _log.debug(f'✓POS {q} @ {after} a.k.a. ␂')
							break
						else:
							char_pre_q = self.view.substr(i_q - 1)
							char_pos_q = None if (i_q+1) >= self.view.__len__() else self.view.substr(i_q + 1)
							if _L: _log.debug(f"{i_q} ? {self.view.__len__()} char_pos_q={char_pos_q}")
							if   char_pre_q == esc_c:
								if _L: _log.debug(f"{esc_c}POS q={q} @ {i_q} pre_char=¦{char_pre_q}¦")
								pass
							elif char_pos_q == q and q in esc_self: # double quote as escape
								if _L: _log.debug(f"••₁{esc_c}POS q={q} @ {i_q} pos_char=¦{char_pos_q}¦ & {esc_self}")
								skip_paired = True
								pass
							else:
								after = i_q
								if _L: _log.debug(f'✓POS {q} @ {after} with pre_char=¦{char_pre_q}¦')
								break

				if before is not None and after is not None: q_size = after - before

			return q_size, before, after

		def replace_region(start, end):
			if sel.size() < end-start-2:
				start += 1; end -= 1
			self.view.sel().subtract(sel)
			self.view.sel().add(sublime.Region(start, end))

		for sel in self.view.sel():
			ctx = self.view.scope_name(sel.a) #e.g., "source.python meta.function…"
			ctx_source = ctx.split()          #      [source.python,meta.function,…]
			esc, esc_self = None, None
			for  ctx_i in ctx_source:         #       source.python
				if esc      is None and ctx_i in self.esc     : esc      = self.esc     .get(ctx_i)
				if esc_self is None and ctx_i in self.esc_self: esc_self = self.esc_self.get(ctx_i)
			if _L: _log.debug(f"{esc}¦{esc_self} {ctx_source}")
			if esc      is None: esc      = self.esc     ['']
			if esc_self is None: esc_self = self.esc_self['']
			if _L: _log.debug(f"{esc}¦{esc_self} {ctx_source}")

			q_res = {}
			for q in self.q_same:
				sz, pre, pos = search_for_quotes(q,q_all[q], esc, esc_self)
				q_res[sz] = (pre,pos)
				if _L: _log.debug(f"q={q} pre={pre} pos={pos} q_all={q_all[q]}")

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
